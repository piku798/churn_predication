# Customer Churn Prediction

A production-ready machine learning project for predicting customer churn using scikit-learn, MLflow, and FastAPI.

## Project Structure

```
churn_prediction/
├── config/
│   └── config.yaml              # Configuration file for all parameters
├── data/
│   ├── raw/                     # Original datasets
│   └── processed/               # Preprocessed datasets
├── notebooks/                   # Jupyter notebooks for exploration
├── src/
│   ├── data/                    # Data loading and preprocessing
│   │   ├── data_loader.py
│   │   ├── data_preprocessing.py
│   │   └── data_validation.py
│   ├── features/                # Feature engineering
│   │   └── feature.py
│   ├── models/                  # Model training
│   │   └── train_model.py
│   ├── pipeline/                # Main ML pipeline
│   │   └── pipeline.py
│   ├── eda/                     # Exploratory data analysis
│   │   └── run_eda.py
│   └── utils/                   # Utilities
│       ├── config_loader.py
│       └── custom_logger.py
├── tests/                       # Unit and integration tests
├── models/                      # Saved model artifacts
├── logs/                        # Application logs
├── .github/workflows/           # GitHub Actions CI/CD
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Multi-container setup
├── requirements.txt             # Python dependencies
├── .pre-commit-config.yaml      # Pre-commit hooks
├── .gitignore                   # Git ignore rules
└── CI_CD_DOCUMENTATION.md       # CI/CD guide
```

## Quick Start

### 1. Clone and Setup

```bash
cd churn_prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks
pip install pre-commit
pre-commit install
```

### 2. Configure Project

Edit `config/config.yaml` with your settings.

### 3. Prepare Data

Place training data at: `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`

### 4. Run Pipeline

```bash
python -c "from src.pipeline.pipeline import run_pipeline; run_pipeline()"
```

### 5. View Results

```bash
mlflow ui
# Visit http://localhost:5000
```

## Development

### Run Tests

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Code Quality

```bash
black src/
isort src/
flake8 src/
pylint src/
```

## Docker

```bash
docker-compose up
```

## CI/CD Pipeline

Automated workflows via GitHub Actions:
- Tests on Python 3.9-3.12
- Code quality checks
- Model training
- Package building

See `CI_CD_DOCUMENTATION.md` for details.

## Configuration

Edit `config/config.yaml` to customize:
- Experiment name and tracking URI
- Target column and test size
- Scaler type and SMOTE strategy
- Model hyperparameters
- Output paths

## Monitoring

### MLflow
- Track experiments at http://localhost:5000
- Compare model metrics
- Access trained artifacts

### Logs
Application logs saved to `logs/` directory.

## Support

See `CI_CD_DOCUMENTATION.md` for comprehensive guide and troubleshooting.
