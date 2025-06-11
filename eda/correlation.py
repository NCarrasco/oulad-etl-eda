import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_correlation_matrix(studentAssessment_df, studentVle_df):
    scores = studentAssessment_df.groupby('id_student')['score'].mean().reset_index()
    activity = studentVle_df.groupby('id_student')['sum_click'].sum().reset_index()
    merged = scores.merge(activity, on='id_student')

    corr = merged.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Matriz de correlación')
    plt.savefig("output/matriz_correlacion.png")
    plt.close()