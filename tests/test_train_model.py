import pandas as pd
from src.models.train_model import train_model


def test_train_model():

    # Create larger balanced sample dataset
    data = {
        "tenure": [10, 20, 30, 15, 25, 35],
        "MonthlyCharges": [70, 80, 90, 60, 85, 95],
        "TotalCharges": [700, 1600, 2700, 900, 2100, 3300],
        "Churn": [0, 1, 0, 1, 0, 1]
    }

    df = pd.DataFrame(data)

    model, scaler = train_model(df)

    assert model is not None
    assert scaler is not None