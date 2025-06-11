from sqlalchemy import text

def test_insert_data_persists_data(sqlite_session):
    # Aquí podrías definir una tabla temporal o simular una insert simple
    # Por ejemplo, insertar un registro dummy y hacer una consulta

    sqlite_session.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
    sqlite_session.execute(text("INSERT INTO test (name) VALUES ('Norman')"))
    result = sqlite_session.execute(text("SELECT * FROM test")).fetchall()

    assert len(result) == 1