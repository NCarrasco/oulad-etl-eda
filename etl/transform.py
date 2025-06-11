# etl/transform.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def clean_dataframes(data_dict: dict):
    for name, df in data_dict.items():
        if isinstance(df, pd.DataFrame):
            df.drop_duplicates(inplace=True)
            df.dropna(how='all', inplace=True)
            df.columns = df.columns.str.strip()


def encode_categorical_columns(studentInfo_df, assessments_df):
    """
    Transforma columnas categóricas en ordinales:
    - gender y final_result en studentInfo
    - assessment_type en assessments
    """
    le_gender = LabelEncoder()
    studentInfo_df['gender_ord'] = le_gender.fit_transform(studentInfo_df['gender'])

    le_result = LabelEncoder()
    studentInfo_df['final_result_ord'] = le_result.fit_transform(studentInfo_df['final_result'])

    le_assessment_type = LabelEncoder()
    assessments_df['assessment_type_ord'] = le_assessment_type.fit_transform(assessments_df['assessment_type'])

    return studentInfo_df, assessments_df
