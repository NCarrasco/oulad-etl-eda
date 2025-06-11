# tests/test_extract.py
import pandas as pd
from io import StringIO
from etl.extract import load_raw_data


def mock_csv_files():
    csv_data = {
        "studentInfo": StringIO("id_student,gender,final_result\n1,M,Pass\n2,F,Fail"),
        "courses": StringIO("code_module,code_presentation\nAAA,2013J")
    }
    return {name: pd.read_csv(content) for name, content in csv_data.items()}


def test_load_raw_data_returns_dict(monkeypatch):
    # Patch pd.read_csv to simulate reading from in-memory CSVs
    mock_data = mock_csv_files()

    def fake_read_csv(path, *args, **kwargs):
        key = path.split("/")[-1].split(".")[0]
        return mock_data.get(key, pd.DataFrame())

    monkeypatch.setattr("pandas.read_csv", fake_read_csv)

    # Usamos cualquier ruta porque está mockeado
    data = load_raw_data("fake_data_dir")
    assert isinstance(data, dict)
    assert "studentInfo" in data
    assert "courses" in data
    assert not data["studentInfo"].empty