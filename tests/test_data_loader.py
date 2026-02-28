import pandas as pd
from src.data.data_loader import load_raw_data
from pathlib import Path


def test_load_raw_data():
    BASE_DIR = Path(__file__).resolve().parents[1]
    file_path = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

    df = load_raw_data(file_path)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty