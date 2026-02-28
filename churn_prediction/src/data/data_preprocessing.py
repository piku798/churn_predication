import pandas as pd
from src.utils.custom_logger import get_logger


logger = get_logger(__name__)


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic preprocessing:
    - Remove duplicate rows
    - Fill missing values
    """

    logger.info("Starting basic preprocessing...")
    df = df.copy()

    # -------------------------
    # 1️⃣ Remove duplicates
    # -------------------------
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        df = df.drop_duplicates()
        logger.info(f"Removed {duplicate_count} duplicate rows")

    # -------------------------
    # 2️⃣ Fill missing values
    # -------------------------

    # Numeric columns → fill with median
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())
            logger.info(f"Filled missing values in numeric column: {col}")

    # Categorical columns → fill with 'Unknown'
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna("Unknown")
            logger.info(f"Filled missing values in categorical column: {col}")

    logger.info("Basic preprocessing completed successfully")

    return df