import pandas as pd
from etl.transform import clean_dataframes, encode_categorical_columns

# test_transform.py
def test_clean_dataframes():
    df = pd.DataFrame({'a': [1, 1, None], 'b': [2, 2, 3]})
    cleaned = clean_dataframes({"dummy_table": df})
    clean_df = cleaned["dummy_table"]

    assert clean_df.isnull().sum().sum() == 0  # sin valores nulos
    assert clean_df.duplicated().sum() == 0    # sin duplicados

def test_encode_categories():
    df_student = pd.DataFrame({'gender': ['M', 'F'], 'final_result': ['Pass', 'Fail']})
    df_assess = pd.DataFrame({'assessment_type': ['TMA', 'CMA']})
    student_res, assess_res = encode_categorical_columns(df_student.copy(), df_assess.copy())
    assert 'gender_ord' in student_res.columns
    assert 'assessment_type_ord' in assess_res.columns
