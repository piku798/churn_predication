import pandas as pd
from src.utils.custom_logger import get_logger

logger = get_logger(__name__)

# Expected schema definition
EXPECTED_SCHEMA = {
    "tenure": "float",
    "MonthlyCharges": "float",
    "TotalCharges": "float",
    "SeniorCitizen": "int",
    "Churn": "object"  # will convert later in preprocessing
}

def validate_data(df: pd.DataFrame) -> dict:
    """
    Perform advanced data validation checks.
    Enforces schema and returns validation report.
    """

    report = {
        "passed": True,
        "warnings": [],
        "errors": []
    }

    # -------------------------
    # 1. Check empty dataset
    # -------------------------
    if df.empty:
        logger.error("Dataset is empty")
        raise ValueError("Dataset is empty")

    # -------------------------
    # 2. Column existence check
    # -------------------------
    for col in EXPECTED_SCHEMA.keys():
        if col not in df.columns:
            msg = f"Missing expected column: {col}"
            logger.error(msg)
            report["errors"].append(msg)
            report["passed"] = False

    if report["errors"]:
        raise ValueError("Critical schema mismatch detected")

    # -------------------------
    # 3. Enforce data types
    # -------------------------
    for col, expected_type in EXPECTED_SCHEMA.items():
        try:
            if expected_type == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")
            elif expected_type == "int":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        except Exception as e:
            msg = f"Failed to convert column {col} to {expected_type}: {e}"
            logger.error(msg)
            report["errors"].append(msg)
            report["passed"] = False

    # -------------------------
    # 4. Duplicate check
    # -------------------------
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        msg = f"{duplicates} duplicate rows found"
        logger.warning(msg)
        report["warnings"].append(msg)
        report["passed"] = False

    # -------------------------
    # 5. Missing value check
    # -------------------------
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if not missing_cols.empty:
        for col, count in missing_cols.items():
            msg = f"Column '{col}' has {count} missing values"
            logger.warning(msg)
            report["warnings"].append(msg)
        report["passed"] = False

    # -------------------------
    # 6. Constant column check
    # -------------------------
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        msg = f"Constant columns detected: {constant_cols}"
        logger.warning(msg)
        report["warnings"].append(msg)
        report["passed"] = False

    # -------------------------
    # 7. Minimum row threshold
    # -------------------------
    MIN_ROWS = 50
    if len(df) < MIN_ROWS:
        msg = f"Dataset has only {len(df)} rows (minimum recommended {MIN_ROWS})"
        logger.warning(msg)
        report["warnings"].append(msg)
        report["passed"] = False

    # -------------------------
    # Final log
    # -------------------------
    if report["passed"]:
        logger.info("Data validation passed with no critical issues")
    else:
        logger.info(
            f"Validation completed with {len(report['warnings'])} warning(s) "
            f"and {len(report['errors'])} error(s)"
        )

    return report