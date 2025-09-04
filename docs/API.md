# TrialMatch AI - API Documentation

## Core Modules

### `src.matching.engine`

#### `TrialMatchEngine`

Main class for matching patients to clinical trials.

**Constructor:**
```python
engine = TrialMatchEngine()
```

**Methods:**

##### `load_trials(trials_data: Dict) -> None`
Load trial data into the matching engine.

**Parameters:**
- `trials_data`: Dictionary of trial data loaded from JSON files

**Example:**
```python
trials = {"trial1.json": {"trial_id": "T001", "criteria": {...}}}
engine.load_trials(trials)
```

##### `match_patient_to_trial(patient: pd.Series, trial_criteria: Dict) -> Tuple[bool, List[str]]`
Match a single patient to a specific trial.

**Parameters:**
- `patient`: Patient data as pandas Series with required fields:
  - `stage`: Cancer stage (I, II, III, IV)
  - `mutation_status`: Mutation status (e.g., "EGFR+", "KRAS G12C+")
  - `performance_status`: ECOG performance status (0-4)
- `trial_criteria`: Trial eligibility criteria dictionary

**Returns:**
- Tuple of (is_match: bool, reasons: List[str])

**Example:**
```python
patient = pd.Series({
    "patient_id": "P001",
    "stage": "IV", 
    "mutation_status": "EGFR+",
    "performance_status": 1
})

criteria = {
    "stage": ["III", "IV"],
    "mutation_required": "EGFR+", 
    "performance_status_max": 2
}

is_match, reasons = engine.match_patient_to_trial(patient, criteria)
```

##### `find_matches_for_patient(patient: pd.Series) -> List[Dict]`
Find all matching trials for a patient.

**Parameters:**
- `patient`: Patient data as pandas Series

**Returns:**
- List of match dictionaries with keys:
  - `trial_file`: Source trial file name
  - `trial_title`: Human readable trial title
  - `trial_id`: Unique trial identifier
  - `is_match`: Boolean match result
  - `reasons`: List of matching reasons/failures
  - `description`: Trial description

### `src.data.loader`

#### `DataLoader`

Handles loading and validation of patient and trial data.

**Constructor:**
```python
loader = DataLoader(data_dir="data")
```

**Methods:**

##### `load_patients(filename: str = "sample_patients.csv") -> pd.DataFrame`
Load patient data from CSV file.

**Returns:**
- DataFrame with patient data

**Required CSV Columns:**
- `patient_id`: Unique identifier
- `age`: Patient age
- `gender`: Male/Female
- `stage`: Cancer stage (I, II, III, IV)
- `mutation_status`: Mutation status
- `smoker`: Boolean smoking history
- `performance_status`: ECOG performance status

##### `load_trials(trial_files: List[str] = None) -> Dict`
Load trial data from JSON files.

**Parameters:**
- `trial_files`: Optional list of trial file paths

**Returns:**
- Dictionary mapping filenames to trial data

**Trial JSON Format:**
```json
{
  "trial_id": "T001",
  "title": "Trial Title",
  "description": "Trial description",
  "criteria": {
    "stage": ["III", "IV"],
    "mutation_required": "EGFR+",
    "performance_status_max": 2
  }
}
```

##### `validate_patient_data(patients: pd.DataFrame) -> bool`
Validate that patient data has required columns.

### `src.utils.pdf_parser`

#### `PDFParser`

AI-powered PDF parsing for clinical trial documents.

**Constructor:**
```python
parser = PDFParser(openai_api_key="your-api-key")
```

**Methods:**

##### `extract_text_from_pdf(pdf_path: str) -> str`
Extract all text from a PDF file.

##### `extract_criteria_sections(pdf_path: str) -> Tuple[List[str], List[str]]`
Extract inclusion and exclusion criteria sections.

**Returns:**
- Tuple of (inclusion_criteria, exclusion_criteria)

##### `interpret_criteria_with_ai(text: str) -> Dict`
Use OpenAI to structure trial criteria from text.

**Returns:**
- Dictionary with structured criteria:
  - `stage`: List of allowed stages
  - `mutation_required`: Required mutations
  - `performance_status_max`: Maximum ECOG score
  - `raw_inclusion`: Raw inclusion criteria text
  - `raw_exclusion`: Raw exclusion criteria text

## Usage Examples

### Basic Patient Matching
```python
from src.data.loader import DataLoader
from src.matching.engine import TrialMatchEngine

# Load data
loader = DataLoader()
patients = loader.load_patients()
trials = loader.load_trials()

# Initialize matching
engine = TrialMatchEngine()
engine.load_trials(trials)

# Find matches for specific patient
patient = patients[patients["patient_id"] == "P1001"].iloc[0]
matches = engine.find_matches_for_patient(patient)

# Print results
for match in matches:
    print(f"Trial: {match['trial_title']}")
    print(f"Match: {match['is_match']}")
    print(f"Reasons: {match['reasons']}")
```

### PDF Analysis Workflow
```python
from src.utils.pdf_parser import PDFParser

parser = PDFParser(api_key="your-openai-key")

# Extract text
text = parser.extract_text_from_pdf("trial_protocol.pdf")

# Get structured criteria
criteria = parser.interpret_criteria_with_ai(text)

# Use criteria for matching
trial_data = {
    "trial_id": "PARSED001",
    "title": "Parsed Trial",
    "criteria": criteria
}
```

## Error Handling

All functions include comprehensive error handling and logging. Common exceptions:

- `FileNotFoundError`: Data files not found
- `ValueError`: Invalid patient/trial data format
- `KeyError`: Missing required data fields
- `JSONDecodeError`: Invalid trial JSON format

Check logs for detailed error information.