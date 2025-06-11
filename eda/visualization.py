import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def generate_all_plots(data):
    os.makedirs("output", exist_ok=True)
    generate_boxplot(data)
    generate_histogram(data)
    generate_scatter(data)
    generate_correlation(data)
    generate_confusion_matrix(data)

def generate_boxplot(data):
    merged = data['studentAssessment'].merge(data['assessments'], on='id_assessment')
    plt.figure(figsize=(10,6))
    sns.boxplot(x='assessment_type', y='score', data=merged)
    plt.title('Distribución de notas por tipo de evaluación')
    plt.savefig("output/boxplot_notas.png")
    plt.close()

def generate_histogram(data):
    activity_per_student = data['studentVle'].groupby('id_student')['sum_click'].sum()
    plt.figure(figsize=(10,6))
    sns.histplot(activity_per_student, bins=30, kde=True)
    plt.title('Distribución de actividad total en el VLE por estudiante')
    plt.xlabel('Total de clics')
    plt.ylabel('Número de estudiantes')
    plt.savefig("output/histograma_actividad.png")
    plt.close()

def generate_scatter(data):
    scores = data['studentAssessment'].groupby('id_student')['score'].mean().reset_index()
    activity = data['studentVle'].groupby('id_student')['sum_click'].sum().reset_index()
    merged_scores = scores.merge(activity, on='id_student')
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='sum_click', y='score', data=merged_scores)
    plt.title('Relación entre actividad en el VLE y nota promedio')
    plt.xlabel('Total de clics en VLE')
    plt.ylabel('Nota promedio')
    plt.savefig("output/dispersion_clicks_vs_score.png")
    plt.close()

def generate_correlation(data):
    scores = data['studentAssessment'].groupby('id_student')['score'].mean().reset_index()
    activity = data['studentVle'].groupby('id_student')['sum_click'].sum().reset_index()
    merged_scores = scores.merge(activity, on='id_student')
    corr = merged_scores.corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Matriz de correlación')
    plt.savefig("output/matriz_correlacion.png")
    plt.close()

def generate_confusion_matrix(data):
    df = data['studentInfo'].copy()
    df['passed'] = (df['final_result'] == 'Pass').astype(int)
    X = df[['gender_ord']]
    y = df['passed']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Matriz de confusión - Aprobado/No aprobado')
    plt.xlabel('Predicción')
    plt.ylabel('Real')
    plt.savefig("output/matriz_confusion.png")
    plt.close()