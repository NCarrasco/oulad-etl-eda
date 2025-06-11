# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base de datos en memoria
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

Base = declarative_base()

@pytest.fixture(scope="function")
def sqlite_session():
    engine = create_engine(SQLALCHEMY_TEST_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()