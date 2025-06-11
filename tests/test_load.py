# tests/test_load.py
import pandas as pd
from sqlalchemy import inspect
from etl.load import create_tables, insert_data

def test_create_tables_creates_tables():
    engine = create_tables()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected = ['courses', 'studentInfo', 'assessments']
    for t in expected:
        assert t in tables

def test_insert_data_persists_data():
    engine = create_tables()
    sample_data = {
        "courses": pd.DataFrame([{"code_module": "M", "code_presentation": "2023", "module_presentation_length": 200}]),
        "studentInfo": pd.DataFrame([{"id_student": 1, "gender": "M", "gender_ord": 1, "final_result": "Pass", "final_result_ord": 0}]),
        "assessments": pd.DataFrame([{
            "id_assessment": 10,
            "code_module": "M",
            "code_presentation": "2023",
            "assessment_type": "TMA",
            "assessment_type_ord": 0,
            "date": 50,
            "weight": 10.0
        }])
    }
    insert_data(engine, sample_data)
    inspector = inspect(engine)
    for table in ["courses", "studentInfo", "assessments"]:
        assert inspector.has_table(table)