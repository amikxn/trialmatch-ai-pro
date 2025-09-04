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
        openai.api_key = openai_api_key
        logger.info("PDFParser initialized")
    
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
        You are a clinical trial document parser. Extract the following from the trial text below:
        - Stage requirements (as list of strings, e.g. ["I", "IIIA"])
        - Required mutations (as list, e.g. ["EGFR", "PD-L1"])
        - Maximum allowed ECOG performance status (integer)
        - Raw inclusion criteria (list of strings)
        - Raw exclusion criteria (list of strings)

        Only return a valid JSON object with the following keys:
        stage, mutation_required, performance_status_max, raw_inclusion, raw_exclusion.

        Trial text:
        {text}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful clinical trial parser."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            parsed = response["choices"][0]["message"]["content"]
            structured = json.loads(parsed)
            logger.info("Successfully parsed criteria with AI")
            return structured
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from AI output: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error in AI interpretation: {e}")
            return {}
