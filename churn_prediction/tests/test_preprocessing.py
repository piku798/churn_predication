from src.data.data_preprocessing import preprocess_data
import pandas as pd


def test_preprocessing_removes_nulls(sample_df):
    df_clean = preprocess_data(sample_df)
    assert df_clean.isnull().sum().sum() == 0