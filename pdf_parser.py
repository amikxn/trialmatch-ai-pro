"""
PDF parsing utilities for clinical trial documents.
"""
import pdfplumber
import openai
import json
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class PDFParser:
    """Handles PDF parsing and AI-powered content extraction."""
    
    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)
        logger.info("PDFParser initialized with new OpenAI client")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text from PDF file."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            logger.info(f"Extracted {len(all_text)} characters from {pdf_path}")
            return all_text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            raise
    
    def extract_criteria_sections(self, pdf_path: str) -> Tuple[List[str], List[str]]:
        """Extract inclusion and exclusion criteria sections."""
        inclusion = []
        exclusion = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    lines = text.split("\n")
                    for line in lines:
                        line_lower = line.lower().strip()
                        if "inclusion" in line_lower and len(line.strip()) > 10:
                            inclusion.append(line.strip())
                        elif "exclusion" in line_lower and len(line.strip()) > 10:
                            exclusion.append(line.strip())
            
            logger.info(f"Extracted {len(inclusion)} inclusion and {len(exclusion)} exclusion criteria")
            return inclusion, exclusion
            
        except Exception as e:
            logger.error(f"Error extracting criteria from PDF {pdf_path}: {e}")
            return [], []
    
    def interpret_criteria_with_ai(self, text: str) -> Dict:
        """Use AI to interpret and structure trial criteria."""
        prompt = f"""
        You are a clinical trial document parser. Extract and structure information from this clinical trial text.
        
        Return ONLY a valid JSON object with these exact keys:
        {{
            "stage": ["I", "II", "III", "IV"],
            "mutation_required": ["EGFR+", "KRAS G12C+", "PD-L1 High"],
            "performance_status_max": 2,
            "raw_inclusion": ["inclusion criteria text 1", "inclusion criteria text 2"],
            "raw_exclusion": ["exclusion criteria text 1", "exclusion criteria text 2"]
        }}
        
        Guidelines:
        - stage: List cancer stages mentioned (I, II, III, IV, IIIA, IIIB, etc.)
        - mutation_required: List specific mutations mentioned (EGFR+, KRAS G12C+, PD-L1 High, etc.)
        - performance_status_max: Maximum ECOG performance status allowed (0-4)
        - raw_inclusion: Key inclusion criteria sentences
        - raw_exclusion: Key exclusion criteria sentences
        
        If information is not clear, use reasonable defaults:
        - stage: ["III", "IV"] for advanced cancer
        - mutation_required: []
        - performance_status_max: 2
        
        Clinical trial text:
        {text[:3000]}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful clinical trial document parser. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=1000
            )

            parsed = response.choices[0].message.content.strip()
            
            # Clean up response - remove any markdown formatting
            if parsed.startswith("```json"):
                parsed = parsed.replace("```json", "").replace("```", "").strip()
            elif parsed.startswith("```"):
                parsed = parsed.replace("```", "").strip()
            
            structured = json.loads(parsed)
            logger.info(f"Successfully parsed criteria with AI: {structured}")
            return structured
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from AI output: {e}")
            logger.error(f"AI Response was: {parsed}")
            # Return a default structure if parsing fails
            return {
                "stage": ["III", "IV"],
                "mutation_required": [],
                "performance_status_max": 2,
                "raw_inclusion": ["Unable to parse inclusion criteria"],
                "raw_exclusion": ["Unable to parse exclusion criteria"]
            }
        except Exception as e:
            logger.error(f"Error in AI interpretation: {e}")
            return {
                "stage": ["III", "IV"],
                "mutation_required": [],
                "performance_status_max": 2,
                "raw_inclusion": ["Error parsing document"],
                "raw_exclusion": ["Error parsing document"]
            }
