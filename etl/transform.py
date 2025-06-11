# etl/transform.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def clean_dataframes(data_dict: dict):
    cleaned = {}
    for name, df in data_dict.items():
        df = df.drop_duplicates()
        df = df.dropna(how="all")
        cleaned[name] = df
    cleaned = encode_ordinal_columns(cleaned)
    return cleaned


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


def encode_ordinal_columns(data: dict) -> dict:
    """
    Codifica columnas categóricas en valores numéricos usando codificación ordinal o label.
    """
    df_info = data.get("studentInfo")
    if df_info is not None:
        # Codificación ordinal personalizada
        age_map = {
            '0-35': 0,
            '35-55': 1,
            '55<=': 2
        }
        education_map = {
            'No Formal quals': 0,
            'Lower Than A Level': 1,
            'A Level or Equivalent': 2,
            'HE Qualification': 3,
            'Post Graduate Qualification': 4
        }
        result_map = {
            'Fail': 0,
            'Withdrawn': 1,
            'Pass': 2,
            'Distinction': 3
        }

        df_info["age_band_ord"] = df_info["age_band"].map(age_map)
        df_info["highest_education_ord"] = df_info["highest_education"].map(education_map)
        df_info["final_result_ord"] = df_info["final_result"].map(result_map)

        # Label encoding para las demás
        for col in ["gender", "region", "disability"]:
            le = LabelEncoder()
            df_info[col + "_ord"] = le.fit_transform(df_info[col].astype(str))

        data["studentInfo"] = df_info

    return data

def generate_fulldomains(dfs: dict) -> dict:
    # Assessment type domain
    assess_types = dfs['assessments']['assessment_type'].dropna().unique()
    df_assess_domain = pd.DataFrame({
        'assessment_type': assess_types,
        'assessment_type_ord': range(len(assess_types))
    })

    # Activity type domain
    if 'vle' in dfs:
        activity_types = dfs['vle']['activity_type'].dropna().unique()
        df_vle_domain = pd.DataFrame({
            'activity_type': activity_types,
            'activity_type_ord': range(len(activity_types))
        })
        dfs['vle_domain'] = df_vle_domain

    dfs['assess_domain'] = df_assess_domain
    return dfs