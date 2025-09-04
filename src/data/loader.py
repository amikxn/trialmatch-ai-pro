"""
Data loading and management functions.
"""
import pandas as pd
import json
import logging
from pathlib import Path
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles loading of patient and trial data."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        logger.info(f"DataLoader initialized with data_dir: {data_dir}")
    
    def load_patients(self, filename: str = "sample_patients.csv") -> pd.DataFrame:
        """Load patient data from CSV file."""
        try:
            filepath = self.data_dir / filename
            patients = pd.read_csv(filepath)
            logger.info(f"Loaded {len(patients)} patients from {filepath}")
            return patients
        except Exception as e:
            logger.error(f"Error loading patients from {filename}: {e}")
            raise
    
    def load_trials(self, trial_files: Optional[List[str]] = None) -> Dict:
        """Load trial data from JSON files."""
        if trial_files is None:
            trial_files = [
                "trials/egfr.json", 
                "trials/pd-l1.json", 
                "trials/kras_g12c.json", 
                "trials/combo.json", 
                "trials/early_stage.json"
            ]
        
        trials = {}
        
        for trial_file in trial_files:
            try:
                filepath = self.data_dir / trial_file
                with open(filepath, 'r') as f:
                    trial_data = json.load(f)
                trials[trial_file] = trial_data
                logger.info(f"Loaded trial from {filepath}")
            except FileNotFoundError:
                logger.warning(f"Trial file {filepath} not found")
            except Exception as e:
                logger.error(f"Error loading trial from {trial_file}: {e}")
        
        logger.info(f"Loaded {len(trials)} total trials")
        return trials
    
    def validate_patient_data(self, patients: pd.DataFrame) -> bool:
        """Validate patient data structure."""
        required_columns = [
            'patient_id', 'age', 'gender', 'stage', 
            'mutation_status', 'smoker', 'performance_status'
        ]
        
        missing_columns = set(required_columns) - set(patients.columns)
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        logger.info("Patient data validation passed")
        return True

