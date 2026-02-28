import pytest
import pandas as pd


@pytest.fixture
def sample_df():
    data = {
        "customerID": ["1", "2", "3"],
        "tenure": [10, None, 5],
        "MonthlyCharges": [70.5, 80.0, None],
        "TotalCharges": [700.0, 800.0, None],
        "Churn": ["Yes", "No", "Yes"]
    }
    return pd.DataFrame(data)