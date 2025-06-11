# etl/load.py
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKeyConstraint
from config.schema import metadata  # Asegúrate de tener un archivo schema.py con los modelos
from sqlalchemy import text

def drop_all_tables_in_order(engine):
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS assessments"))
        conn.execute(text("DROP TABLE IF EXISTS studentInfo"))
        conn.execute(text("DROP TABLE IF EXISTS courses"))
        conn.commit()


def create_tables(engine):
    metadata.create_all(engine)

    Table('courses', metadata,
        Column('code_module', String(20), primary_key=True),
        Column('code_presentation', String(20), primary_key=True),
        Column('module_presentation_length', Integer)
    )

    Table('studentInfo', metadata,
        Column('id_student', Integer, primary_key=True),
        Column('gender', String(10)),
        Column('gender_ord', Integer),
        Column('final_result', String(20)),
        Column('final_result_ord', Integer)
    )

    Table('assessments', metadata,
        Column('id_assessment', Integer, primary_key=True),
        Column('code_module', String(20)),
        Column('code_presentation', String(20)),
        Column('assessment_type', String(20)),
        Column('assessment_type_ord', Integer),
        Column('date', Integer),
        Column('weight', Float),
        ForeignKeyConstraint(['code_module', 'code_presentation'], ['courses.code_module', 'courses.code_presentation'])
    )

    metadata.create_all(engine)
    return engine


def insert_data(engine, data):
    # Elimina tablas en orden correcto
    drop_all_tables_in_order(engine)

    # Inserta data
    data['courses'].to_sql('courses', engine, if_exists='replace', index=False, chunksize=500)
    data['studentInfo'].to_sql('studentInfo', engine, if_exists='replace', index=False, chunksize=500)
    data['assessments'].to_sql('assessments', engine, if_exists='replace', index=False, chunksize=500)
    data["studentAssessment"].to_sql("studentAssessment", engine, if_exists='replace', index=False, chunksize=500)
    data["studentVle"].to_sql("studentVle", engine, if_exists='replace', index=False, chunksize=500)
    data["studentRegistration"].to_sql("studentRegistration", engine, if_exists='replace', index=False, chunksize=500)
    data["vle"].to_sql("vle", engine, if_exists='replace', index=False, chunksize=500)
