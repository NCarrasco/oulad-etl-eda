import pandas as pd


def generate_summary_stats(data):
    """
    Imprime un resumen estadístico simple para score y sum_click por estudiante.
    """
    print("\n📈 Estadísticas de Score (studentAssessment):")
    print(data['studentAssessment']['score'].describe())

    print("\n📈 Estadísticas de sum_click (studentVle):")
    print(data['studentVle']['sum_click'].describe())