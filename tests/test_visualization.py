# tests/test_visualization.py
import os
import shutil
import pandas as pd
from eda.visualization import generate_all_plots

def test_generate_all_plots_creates_files(tmp_path):
    sample_data = {
        "studentInfo": pd.DataFrame({
            "id_student": [1, 2],
            "gender": ["M", "F"],
            "gender_ord": [1, 0],
            "final_result": ["Pass", "Fail"],
            "final_result_ord": [1, 0]
        }),
        "assessments": pd.DataFrame({
            "id_assessment": [1, 2],
            "assessment_type": ["TMA", "CMA"],
            "assessment_type_ord": [0, 1]
        }),
        "studentAssessment": pd.DataFrame({
            "id_student": [1, 2],
            "id_assessment": [1, 2],
            "score": [85.0, 60.0]
        }),
        "studentVle": pd.DataFrame({
            "id_student": [1, 2],
            "sum_click": [120, 80]
        })
    }

    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    generate_all_plots(sample_data)

    expected_files = [
        "boxplot_notas.png",
        "histograma_actividad.png",
        "dispersion_clicks_vs_score.png",
        "matriz_correlacion.png",
        "matriz_confusion.png"
    ]
    for f in expected_files:
        assert os.path.exists(os.path.join(output_dir, f))