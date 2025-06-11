# tests/test_extract.py
import os
from etl.extract import load_raw_data

def test_load_raw_data_returns_dict():
    data = load_raw_data()
    assert isinstance(data, dict)
    expected_keys = ['studentInfo', 'studentRegistration', 'assessments',
                     'studentAssessment', 'vle', 'studentVle', 'courses']
    for key in expected_keys:
        assert key in data
        assert not data[key].empty

def test_data_directory_exists():
    assert os.path.exists("data/raw")