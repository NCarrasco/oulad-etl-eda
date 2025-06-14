import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_correlation_matrix(studentInfo_df, studentVle_df, studentAssessment_df):

    # Agrupar score promedio por estudiante
    scores = studentAssessment_df.groupby('id_student')['score'].mean().reset_index()

    # Agrupar clics totales por estudiante
    clicks = studentVle_df.groupby('id_student')['sum_click'].sum().reset_index()

    # Merge general con studentInfo
    merged_df = studentInfo_df.merge(scores, on='id_student', how='left')
    merged_df = merged_df.merge(clicks, on='id_student', how='left')

    # Convertir variables categóricas a numéricas para correlación
    ordinal_columns = ['gender_ord', 'final_result_ord']
    numeric_columns = ['studied_credits', 'num_of_prev_attempts', 'score', 'sum_click']
    columns_for_corr = ordinal_columns + numeric_columns

    # Filtrar solo columnas necesarias
    corr_df = merged_df[columns_for_corr].dropna()

    # Calcular y graficar matriz de correlación
    correlation_matrix = corr_df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title("Matriz de Correlación")
    plt.tight_layout()

    # Guardar imagen en output/eda
    output_path = os.path.join("output", "eda", "correlation_matrix.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    ##plt.savefig(output_path)
    plt.savefig("output/eda/correlation_matrix.png")
    plt.close()