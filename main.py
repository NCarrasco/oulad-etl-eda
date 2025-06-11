import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKeyConstraint
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os

# 1. CARGA DE DATOS
studentInfo = pd.read_csv('studentInfo.csv')
studentRegistration = pd.read_csv('studentRegistration.csv')
assessments = pd.read_csv('assessments.csv')
studentAssessment = pd.read_csv('studentAssessment.csv')
vle = pd.read_csv('vle.csv')
studentVle = pd.read_csv('studentVle.csv')
courses = pd.read_csv('courses.csv')

# 2. LIMPIEZA DE DATOS
for df in [studentInfo, studentRegistration, assessments, studentAssessment, vle, studentVle, courses]:
    df.drop_duplicates(inplace=True)
    df.ffill(inplace=True)

# 3. TRANSFORMACIÓN DE VARIABLES CATEGÓRICAS A ORDINALES
le_gender = LabelEncoder()
studentInfo['gender_ord'] = le_gender.fit_transform(studentInfo['gender'])

le_result = LabelEncoder()
studentInfo['final_result_ord'] = le_result.fit_transform(studentInfo['final_result'])

le_assessment_type = LabelEncoder()
assessments['assessment_type_ord'] = le_assessment_type.fit_transform(assessments['assessment_type'])

# 4. DEFINICIÓN DEL MODELO RELACIONAL
engine = create_engine('mysql+mysqlconnector://root:Admin.123@localhost/ouladdb', echo=True)
metadata = MetaData()

courses_tbl = Table('courses', metadata,
    Column('code_module', String(20), primary_key=True),
    Column('code_presentation', String(20), primary_key=True),
    Column('module_presentation_length', Integer)
)

student_info_tbl = Table('studentInfo', metadata,
    Column('id_student', Integer, primary_key=True),
    Column('gender', String(10)),
    Column('gender_ord', Integer),
    Column('final_result', String(20)),
    Column('final_result_ord', Integer)
)

assessments_tbl = Table('assessments', metadata,
    Column('id_assessment', Integer, primary_key=True),
    Column('code_module', String(20)),
    Column('code_presentation', String(20)),
    Column('assessment_type', String(20)),
    Column('assessment_type_ord', Integer),
    Column('date', Integer),
    Column('weight', Float),
    ForeignKeyConstraint(['code_module', 'code_presentation'], ['courses.code_module', 'courses.code_presentation'])
)

# Crear las tablas respetando el orden de las dependencias
metadata.create_all(engine)

# 5. CARGA DE DATOS A LA BASE DE DATOS
courses.to_sql('courses', engine, if_exists='replace', index=False)
studentInfo.to_sql('studentInfo', engine, if_exists='replace', index=False)
assessments.to_sql('assessments', engine, if_exists='replace', index=False)

# 6. FULLDOMAIN Y EDA
os.makedirs("output", exist_ok=True)

# a) Boxplot de notas por tipo de evaluación
merged = studentAssessment.merge(assessments, on='id_assessment')
plt.figure(figsize=(10,6))
sns.boxplot(x='assessment_type', y='score', data=merged)
plt.title('Distribución de notas por tipo de evaluación')
plt.savefig("output/boxplot_notas.png")
plt.close()

# b) Histograma de actividad en el VLE
activity_per_student = studentVle.groupby('id_student')['sum_click'].sum()
plt.figure(figsize=(10,6))
sns.histplot(activity_per_student, bins=30, kde=True)
plt.title('Distribución de actividad total en el VLE por estudiante')
plt.xlabel('Total de clics')
plt.ylabel('Número de estudiantes')
plt.savefig("output/histograma_actividad.png")
plt.close()

# c) Relación entre actividad en el VLE y nota promedio
scores = studentAssessment.groupby('id_student')['score'].mean().reset_index()
activity = studentVle.groupby('id_student')['sum_click'].sum().reset_index()
merged_scores = scores.merge(activity, on='id_student')
plt.figure(figsize=(10,6))
sns.scatterplot(x='sum_click', y='score', data=merged_scores)
plt.title('Relación entre actividad en el VLE y nota promedio')
plt.xlabel('Total de clics en VLE')
plt.ylabel('Nota promedio')
plt.savefig("output/dispersion_clicks_vs_score.png")
plt.close()

# d) Matriz de correlación
corr = merged_scores.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Matriz de correlación')
plt.savefig("output/matriz_correlacion.png")
plt.close()

# e) Matriz de confusión - Aprobado/No aprobado
studentInfo['passed'] = (studentInfo['final_result'] == 'Pass').astype(int)
X = studentInfo[['gender_ord']]
y = studentInfo['passed']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = LogisticRegression()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de confusión - Aprobado/No aprobado')
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.savefig("output/matriz_confusion.png")
plt.close()

print("✅ ETL y EDA completados. Resultados guardados en la carpeta 'output'.")