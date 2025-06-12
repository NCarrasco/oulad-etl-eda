# eda/stats_summary.py
import pandas as pd
from scipy.stats import kurtosis, skew
from pathlib import Path

def generate_summary_stats(dataframes: dict, output_path: str = "output/eda/summary_stats.csv"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for name, df in dataframes.items():
            f.write(f"\n--- {name.upper()} ---\n")
            numeric_df = df.select_dtypes(include='number')

            if numeric_df.empty:
                f.write("Sin columnas numéricas.\n\n")
                continue

            summary = numeric_df.describe().T
            summary["kurtosis"] = numeric_df.kurtosis()
            summary["skew"] = numeric_df.skew()

            summary.to_csv(f)
            f.write("\n")

    print(f"✅ Estadísticas guardadas en {output_path}")