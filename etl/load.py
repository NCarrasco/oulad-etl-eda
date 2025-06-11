# etl/load.py
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKeyConstraint

def create_tables():
    engine = create_engine('mysql+mysqlconnector://root:Admin.123@localhost/ouladdb', echo=True)
    metadata = MetaData()

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
    data['courses'].to_sql('courses', engine, if_exists='replace', index=False)
    data['studentInfo'].to_sql('studentInfo', engine, if_exists='replace', index=False)
    data['assessments'].to_sql('assessments', engine, if_exists='replace', index=False)