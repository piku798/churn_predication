from src.features.feature import feature_engineering


def test_feature_engineering(sample_df):
    df_fe = feature_engineering(sample_df)

    assert "customerID" not in df_fe.columns
    assert df_fe["Churn"].isin([0, 1]).all()