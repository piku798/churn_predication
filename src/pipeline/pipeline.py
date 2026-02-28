from pathlib import Path

from src.data.data_loader import load_raw_data
from src.data.data_validation import validate_data
from src.data.data_preprocessing import preprocess_data
from src.features.feature import feature_engineering
from src.models.train_model import train_model


def run_pipeline():
    """
    Full pipeline:
    Load → Validate → Preprocess → Feature Engineering → Train
    """

    BASE_DIR = Path(__file__).resolve().parents[2]
    file_path = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

    # --------------------
    # Load Data
    # --------------------
    df = load_raw_data(file_path)

    # --------------------
    # Validate
    # --------------------
    validate_data(df)

    # --------------------
    # Preprocess
    # --------------------
    df = preprocess_data(df)

    # Validate again (optional)
    validate_data(df)

    # --------------------
    # Feature Engineering
    # --------------------
    df = feature_engineering(df)

    # --------------------
    # Train Model
    # --------------------
    train_model(df)

    return df


if __name__ == "__main__":
    run_pipeline()