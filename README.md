## 🧠📈 Caso Práctico 3 – OULAD - ETL & EDA con Ciencia de Datos

Maestría en Ciencia de Datos e Inteligencia Artificial (MACDIA)
Materia: Ciencia de Datos I – INF-7303-C1
Profesor: Silverio Del Orbe A.

---

## 🎯 Objetivo del Proyecto

Este repositorio contiene la solución al caso práctico 3 de la Maestría en Ciencia de Datos e Inteligencia Artificial (MACDIA) Materia: Ciencia de Datos I – INF-7303-C1 ```Profesor:``` `Silverio Del Orbe A.`

El objetivo principal es realizar un proceso completo de ETL (Extracción, Transformación y Carga) del dataset OULAD y desarrollar un Análisis Exploratorio de Datos (EDA) extendido utilizando Python. Incluye:

* Limpieza y transformación de los datos.
* Creación de claves primarias y foráneas.
* Codificación ordinal de variables categóricas.
* Carga en base de datos relacional (MySQL).
* FullDomain en las tablas ASSESS y VLE.
* Visualizaciones (boxplot, histograma, scatter, matriz de correlación, matriz de confusión).

---

## 🛠️ Arquitectura de la Solución

##### La solución está organizada de la siguiente manera:

```
oulad-etl-eda/
├── data/                    # CSVs originales del dataset OULAD
├── output/                  # Resultados del EDA (gráficas, matrices)
├── scripts/
│   ├── main.py              # Script principal que ejecuta todo el proceso
├── schema.sql              # Script SQL para crear el esquema relacional
├── requirements.txt        # Dependencias del proyecto en Python
├── README.md               # Documentación del proyecto
```

---

###  🔧 Stack Tecnológico

| Componente      | Tecnología          |
| --------------- | ------------------- |
| ETL + EDA       | Python 3.12         |
| Visualizaciones | Matplotlib, Seaborn |
| Base de Datos   | MySQL               |
| IDE             | PyCharm / VS Code   |

---

##### 🌟 Criterios de Evaluación Cubiertos

| Criterio                            | Cumplido |
| ----------------------------------- | -------- |
| Montar el OULAD en un DBMS          | ✅        |
| ETL orquestado con transformaciones | ✅        |
| FullDomain de ASSESS y VLE          | ✅        |
| EDA extendido con visualizaciones   | ✅        |
| Documentación clara y organizada    | ✅        |

---

###  `📆 Dataset`

El dataset OULAD está disponible para descarga desde la página oficial:
[https://analyse.kmi.open.ac.uk/open\_dataset](https://analyse.kmi.open.ac.uk/open_dataset)

Una vez descargado, colóquelo en la carpeta `data/`.

---

## # ```🚀 Cómo Ejecutar el Proyecto```

##### 1. Clonar el repositorio:

```bash
git clone https://github.com/tu_usuario/oulad-etl-eda.git
cd oulad-etl-eda
```

##### 2. Crear entorno virtual y activar:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

##### 3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

##### 4. Crear la base de datos `ouladdb` en MySQL manualmente:

```sql
CREATE DATABASE ouladdb;
```

##### 5. Ejecutar el script principal:

```bash
python scripts/main.py
```

#### Los resultados se guardarán en la carpeta `output/`.

---

### 🔹 Autores

* Norman Yulifer Carrasco Medina
* Miguel Mariano Pimentel Alcántara
* Miguel Ángel Consoro Guzmán
---

#### 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

#### 📓 Referencias

* [https://pandas.pydata.org/](https://pandas.pydata.org/)
* [https://scikit-learn.org/](https://scikit-learn.org/)
* [https://matplotlib.org/](https://matplotlib.org/)
* [https://seaborn.pydata.org/](https://seaborn.pydata.org/)
* [https://dev.mysql.com/](https://dev.mysql.com/)
