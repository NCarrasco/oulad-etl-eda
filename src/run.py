# src/run.py
from etl.extract import load_raw_data
from etl.transform import clean_dataframes, encode_categorical_columns
from etl.load import create_tables, insert_data
from eda.visualization import generate_all_plots
from config.settings import SQLALCHEMY_URL, DATA_DIR
from common.logger import setup_logger
from sqlalchemy import create_engine
from eda.stats_summary import generate_summary_stats
from eda.correlation import plot_correlation_matrix

logger = setup_logger("OULAD")

if __name__ == "__main__":
    logger.info("📦 Iniciando proceso ETL...")

    # 1. Carga de datos
    raw_data = load_raw_data(DATA_DIR)

    # 2. Limpieza
    clean_dataframes(raw_data)

    # 3. Transformación categórica
    raw_data['studentInfo'], raw_data['assessments'] = encode_categorical_columns(
        raw_data['studentInfo'], raw_data['assessments']
    )

    # 4. Crear engine y tablas
    engine = create_engine(SQLALCHEMY_URL, echo=True)
    create_tables(engine)

    # 5. Insertar datos
    insert_data(engine, raw_data)

    logger.info("📊 Generando visualizaciones EDA...")
    generate_all_plots(raw_data)
    generate_summary_stats(raw_data)
    plot_correlation_matrix(
        raw_data["studentInfo"],
        raw_data["studentVle"],
        raw_data["studentAssessment"]  # <--- Agrega este argumento
    )

    logger.info("✅ Proceso finalizado. Revisa la carpeta 'output'.")