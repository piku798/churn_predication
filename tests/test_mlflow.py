import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load data
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# Start MLflow tracking
with mlflow.start_run():

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Log parameter
    mlflow.log_param("max_iter", 200)

    # Log metric
    mlflow.log_metric("accuracy", acc)

    # Log model
    mlflow.sklearn.log_model(model, name="model")

print("Done")