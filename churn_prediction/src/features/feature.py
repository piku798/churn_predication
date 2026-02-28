import pandas as pd
from sklearn.preprocessing import LabelEncoder
from src.utils.custom_logger import get_logger

logger = get_logger(__name__)


def feature_engineering(df: pd.DataFrame, target_column: str = "Churn") -> pd.DataFrame:
    """
    Perform automatic feature engineering:
    - Drop ID column
    - Encode target column
    - Detect categorical columns
    - Label encode binary categorical columns
    - One-hot encode multi-category categorical columns
    """

    logger.info("Starting feature engineering...")
    df = df.copy()

    # ----------------------------------
    # 1️⃣ Drop ID column if exists
    # ----------------------------------
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)
        logger.info("Dropped customerID column")

    # ----------------------------------
    # 2️⃣ Encode Target Column
    # ----------------------------------
    if target_column in df.columns and df[target_column].dtype == "object":
        df[target_column] = df[target_column].map({"Yes": 1, "No": 0})
        logger.info("Encoded target column")

    # ----------------------------------
    # 3️⃣ Detect categorical columns
    # ----------------------------------
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # Remove target if still object
    if target_column in categorical_cols:
        categorical_cols.remove(target_column)

    logger.info(f"Categorical columns detected: {categorical_cols}")

    # ----------------------------------
    # 4️⃣ Process each categorical column
    # ----------------------------------
    for col in categorical_cols:

        unique_values = df[col].nunique()

        # If binary categorical → Label Encoding
        if unique_values == 2:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            logger.info(f"Label encoded binary column: {col}")

        # If more than 2 categories → One Hot Encoding
        else:
            df = pd.get_dummies(df, columns=[col], drop_first=True)
            logger.info(f"One-hot encoded column: {col}")

    logger.info("Feature engineering completed successfully")

    return df