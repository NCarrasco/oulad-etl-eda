# etl/extract.py
import pandas as pd
import os

def load_raw_data(data_dir):
    files = [
        'studentInfo.csv', 'studentRegistration.csv', 'assessments.csv',
        'studentAssessment.csv', 'vle.csv', 'studentVle.csv', 'courses.csv'
    ]
    data = {}
    for file in files:
        path = os.path.join(data_dir, file)
        data[file.split('.')[0]] = pd.read_csv(path)
    return data
