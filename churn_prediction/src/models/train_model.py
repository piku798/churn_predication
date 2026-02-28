import joblib
from pathlib import Path

import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

from imblearn.over_sampling import SMOTE

from src.utils.config_loader import load_config
from src.utils.custom_logger import get_logger


logger = get_logger(__name__)


def train_model(df):

    logger.info("Starting Model Training Pipeline")

    config = load_config()
    logger.info("Configuration loaded successfully")

    target_column = config["data"]["target_column"]
    test_size = config["data"]["test_size"]
    random_state = config["data"]["random_state"]

    smote_config = config["smote"]
    scaler_config = config["scaler"]
    model_config = config["model"]
    path_config = config["paths"]
    mlflow_config = config["mlflow"]

    X = df.drop(target_column, axis=1)
    y = df[target_column]

    logger.info(f"Target column: {target_column}")
    logger.info(f"Dataset shape: {df.shape}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    logger.info("Train-test split completed")

    # ---------------- MLflow Start ----------------
    mlflow.set_tracking_uri(mlflow_config["tracking_uri"])
    mlflow.set_experiment(mlflow_config["experiment_name"])

    with mlflow.start_run():

        # Log parameters
        mlflow.log_params(model_config)
        mlflow.log_param("scaler_type", scaler_config["type"])
        mlflow.log_param("smote_sampling_strategy", smote_config["sampling_strategy"])
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("random_state", random_state)

        # ---------------- Scaling ----------------
        if scaler_config["type"] == "standard":
            scaler = StandardScaler()
            logger.info("Using StandardScaler")
        else:
            scaler = MinMaxScaler()
            logger.info("Using MinMaxScaler")

        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # ---------------- SMOTE ----------------
        smote = SMOTE(
            random_state=smote_config["random_state"],
            sampling_strategy=smote_config["sampling_strategy"]
        )

        X_train_resampled, y_train_resampled = smote.fit_resample(
            X_train_scaled,
            y_train
        )

        logger.info("SMOTE applied")

        # ---------------- Model ----------------
        model = LogisticRegression(
            max_iter=model_config["max_iter"],
            C=model_config["C"],
            solver=model_config["solver"]
        )

        model.fit(X_train_resampled, y_train_resampled)

        logger.info("Model training completed")

        # ---------------- Evaluation ----------------
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]

        roc_score = roc_auc_score(y_test, y_proba)
        report = classification_report(y_test, y_pred, zero_division=0)

        logger.info(f"\nClassification Report:\n{report}")
        logger.info(f"ROC-AUC Score: {roc_score:.4f}")

        # Log metrics
        mlflow.log_metric("roc_auc", roc_score)

        # Log model artifact
        mlflow.sklearn.log_model(model, name="model")

    # ---------------- Save Local Copy ----------------
    BASE_DIR = Path(__file__).resolve().parents[2]
    model_dir = BASE_DIR / path_config["model_dir"]
    model_dir.mkdir(exist_ok=True)

    joblib.dump(model, model_dir / path_config["model_name"])
    joblib.dump(scaler, model_dir / path_config["scaler_name"])

    logger.info("Model and scaler saved successfully")
    logger.info("Training pipeline finished successfully")

    return model, scaler