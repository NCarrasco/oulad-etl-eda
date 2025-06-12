# src/run.py
from etl.extract import load_raw_data
from etl.transform import clean_dataframes, encode_categorical_columns
from etl.load import create_tables, insert_data
from eda.visualization import (
    generate_all_plots,
    plot_scatter_plots,
    plot_gaussian_distribution,
    plot_kurtosis_skewness_barplots
)
from config.settings import SQLALCHEMY_URL, DATA_DIR
from common.logger import setup_logger
from sqlalchemy import create_engine
from eda.stats_summary import generate_summary_stats
from eda.correlation import plot_correlation_matrix
from etl.transform import generate_fulldomain_summary


logger = setup_logger("OULAD")

if __name__ == "__main__":
    logger.info("📦 Iniciando proceso ETL...")

    # 1. Carga de datos
    raw_data = load_raw_data(DATA_DIR)

    # 2. Limpieza y transformación completa
    cleaned_data = clean_dataframes(raw_data)

    # 3. Generar resumen de dominios antes de codificar
    generate_fulldomain_summary(cleaned_data)

    # 4. Codificación ordinal de variables categóricas
    cleaned_data['studentInfo'], cleaned_data['assessments'] = encode_categorical_columns(
        cleaned_data['studentInfo'], cleaned_data['assessments']
    )

    # 5. Crear engine y tablas
    engine = create_engine(SQLALCHEMY_URL, echo=True)
    create_tables(engine)

    # 6. Insertar datos
    insert_data(engine, cleaned_data)

    # 7. Visualizaciones
    logger.info("📊 Generando visualizaciones EDA...")
    generate_all_plots(cleaned_data)
    generate_summary_stats(cleaned_data)
    plot_kurtosis_skewness_barplots(cleaned_data["studentInfo"])
    plot_correlation_matrix(
        cleaned_data["studentInfo"],
        cleaned_data["studentVle"],
        cleaned_data["studentAssessment"]
    )
    plot_scatter_plots(
        cleaned_data["studentInfo"],
        cleaned_data["studentVle"],
        cleaned_data["studentAssessment"]
    )
    plot_gaussian_distribution(cleaned_data["studentAssessment"])

    logger.info("✅ Proceso finalizado. Revisa la carpeta 'output'.")