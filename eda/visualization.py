import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from scipy.stats import kurtosis, skew



def generate_all_plots(data):
    os.makedirs("output", exist_ok=True)
    generate_boxplot(data)
    generate_histogram(data)
    generate_scatter(data)
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


def plot_scatter_plots(studentInfo_df, studentVle_df, studentAssessment_df):
    # Agrupar score promedio y clics por estudiante
    scores = studentAssessment_df.groupby('id_student')['score'].mean().reset_index()
    clicks = studentVle_df.groupby('id_student')['sum_click'].sum().reset_index()

    # Merge con studentInfo
    merged_df = studentInfo_df.merge(scores, on='id_student', how='left')
    merged_df = merged_df.merge(clicks, on='id_student', how='left')

    # Crear carpeta de salida
    output_dir = os.path.join("output", "eda")
    os.makedirs(output_dir, exist_ok=True)

    # Scatter plot 1: sum_click vs score
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=merged_df, x='sum_click', y='score', hue='final_result_ord', palette='viridis')
    plt.title('Relación entre Clics y Calificación')
    plt.xlabel('Total de Clics')
    plt.ylabel('Puntaje Promedio')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'scatter_clicks_vs_score.png'))
    plt.close()

    # Scatter plot 2: studied_credits vs score
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=merged_df, x='studied_credits', y='score', hue='final_result_ord', palette='magma')
    plt.title('Créditos Estudiados vs Puntaje Promedio')
    plt.xlabel('Créditos Estudiados')
    plt.ylabel('Puntaje Promedio')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'scatter_credits_vs_score.png'))
    plt.close()

    #campana de Gauss basada en la variable score (puntaje)
def plot_gaussian_distribution(studentAssessment_df: pd.DataFrame):
    # Filtramos valores nulos y tomamos la columna de interés
    scores = studentAssessment_df['score'].dropna()

    # Creamos el gráfico
    plt.figure(figsize=(10, 6))
    sns.histplot(scores, kde=True, bins=50, color='skyblue', edgecolor='black')
    plt.title("Distribución tipo Campana de Gauss - Score")
    plt.xlabel("Puntaje")
    plt.ylabel("Frecuencia")

    # Guardamos el gráfico
    output_path = os.path.join("output", "eda", "campana_gauss_score.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def plot_kurtosis_skewness_barplots(df: pd.DataFrame, output_dir="output/eda"):
    # Filtrar solo columnas numéricas
    numeric_df = df.select_dtypes(include='number')

    # Calcular kurtosis y skewness
    kurtosis_vals = numeric_df.apply(lambda x: kurtosis(x.dropna()))
    skew_vals = numeric_df.apply(lambda x: skew(x.dropna()))

    # Crear carpeta de salida
    os.makedirs(output_dir, exist_ok=True)

    # Graficar kurtosis
    plt.figure(figsize=(12, 6))
    sns.barplot(x=kurtosis_vals.index, y=kurtosis_vals.values, palette="viridis")
    plt.xticks(rotation=45)
    plt.title("Kurtosis por Variable Numérica")
    plt.ylabel("Kurtosis")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "kurtosis_barplot.png"))
    plt.close()

    # Graficar skewness
    plt.figure(figsize=(12, 6))
    sns.barplot(x=skew_vals.index, y=skew_vals.values, palette="magma")
    plt.xticks(rotation=45)
    plt.title("Asimetría (Skewness) por Variable Numérica")
    plt.ylabel("Skewness")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "skewness_barplot.png"))
    plt.close()