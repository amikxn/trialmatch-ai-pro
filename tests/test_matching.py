"""
Unit tests for the matching engine.
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.matching.engine import TrialMatchEngine
from src.data.loader import DataLoader

class TestTrialMatchEngine:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.engine = TrialMatchEngine()
        
        # Sample trial data for testing
        self.test_trials = {
            "test_egfr.json": {
                "trial_id": "TEST001",
                "title": "Test EGFR Trial",
                "description": "Test trial for EGFR patients",
                "criteria": {
                    "mutation_required": "EGFR+",
                    "stage": ["III", "IV"],
                    "performance_status_max": 1
                }
            },
            "test_kras.json": {
                "trial_id": "TEST002", 
                "title": "Test KRAS Trial",
                "description": "Test trial for KRAS patients",
                "criteria": {
                    "mutation_required": "KRAS G12C+",
                    "stage": ["IV"],
                    "performance_status_max": 2
                }
            }
        }
        
        self.engine.load_trials(self.test_trials)
        
        # Sample patient data
        self.test_patient_match = pd.Series({
            "patient_id": "TEST_P001",
            "age": 65,
            "gender": "Female", 
            "stage": "IV",
            "mutation_status": "EGFR+",
            "smoker": True,
            "performance_status": 1
        })
        
        self.test_patient_no_match = pd.Series({
            "patient_id": "TEST_P002",
            "age": 45,
            "gender": "Male",
            "stage": "I", 
            "mutation_status": "None",
            "smoker": False,
            "performance_status": 0
        })

    def test_engine_initialization(self):
        """Test that engine initializes correctly."""
        engine = TrialMatchEngine()
        assert engine.trials == {}
        
    def test_load_trials(self):
        """Test loading trial data."""
        assert len(self.engine.trials) == 2
        assert "test_egfr.json" in self.engine.trials
        
    def test_patient_matches_egfr_trial(self):
        """Test patient that should match EGFR trial."""
        criteria = self.test_trials["test_egfr.json"]["criteria"]
        is_match, reasons = self.engine.match_patient_to_trial(
            self.test_patient_match, criteria
        )
        
        assert is_match == True
        assert "Meets all inclusion criteria" in reasons
        
    def test_patient_fails_stage_requirement(self):
        """Test patient that fails stage requirement."""
        criteria = self.test_trials["test_kras.json"]["criteria"]  # Requires stage IV
        patient_wrong_stage = self.test_patient_match.copy()
        patient_wrong_stage["stage"] = "I"  # Wrong stage
        
        is_match, reasons = self.engine.match_patient_to_trial(
            patient_wrong_stage, criteria
        )
        
        assert is_match == False
        assert any("stage" in reason.lower() for reason in reasons)
        
    def test_patient_fails_mutation_requirement(self):
        """Test patient that fails mutation requirement.""" 
        criteria = self.test_trials["test_egfr.json"]["criteria"]
        patient_wrong_mutation = self.test_patient_match.copy()
        patient_wrong_mutation["mutation_status"] = "KRAS G12C+"  # Wrong mutation
        
        is_match, reasons = self.engine.match_patient_to_trial(
            patient_wrong_mutation, criteria
        )
        
        assert is_match == False
        assert any("mutation" in reason.lower() for reason in reasons)
        
    def test_patient_fails_performance_status(self):
        """Test patient that fails performance status requirement."""
        criteria = self.test_trials["test_egfr.json"]["criteria"]  # Max PS = 1
        patient_poor_ps = self.test_patient_match.copy()
        patient_poor_ps["performance_status"] = 3  # Too high
        
        is_match, reasons = self.engine.match_patient_to_trial(
            patient_poor_ps, criteria
        )
        
        assert is_match == False
        assert any("performance status" in reason.lower() for reason in reasons)
        
    def test_find_matches_for_patient(self):
        """Test finding all matches for a patient."""
        matches = self.engine.find_matches_for_patient(self.test_patient_match)
        
        assert len(matches) == 2  # Should check against both trials
        
        # Should match EGFR trial
        egfr_match = next(m for m in matches if "EGFR" in m["trial_title"])
        assert egfr_match["is_match"] == True
        
        # Should not match KRAS trial (wrong mutation)
        kras_match = next(m for m in matches if "KRAS" in m["trial_title"])
        assert kras_match["is_match"] == False

class TestDataLoader:
    
    def test_data_loader_initialization(self):
        """Test DataLoader initializes correctly."""
        loader = DataLoader()
        assert str(loader.data_dir) == "data"
        
    def test_validate_patient_data(self):
        """Test patient data validation."""
        loader = DataLoader()
        
        # Valid data
        valid_data = pd.DataFrame({
            'patient_id': ['P001'],
            'age': [65],
            'gender': ['Female'],
            'stage': ['IV'],
            'mutation_status': ['EGFR+'],
            'smoker': [True],
            'performance_status': [1]
        })
        
        assert loader.validate_patient_data(valid_data) == True
        
        # Invalid data (missing column)
        invalid_data = pd.DataFrame({
            'patient_id': ['P001'],
            'age': [65]
            # Missing other required columns
        })
        
        assert loader.validate_patient_data(invalid_data) == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
