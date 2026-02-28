# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions for continuous integration and deployment, combined with Docker for containerization. The pipeline ensures code quality, runs comprehensive tests, trains models, and provides artifact management.

## Pipeline Components

### 1. Main CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

**Triggers:** Push to master/main/develop, Pull Requests

**Jobs:**

#### Test Suite
- Runs on Python 3.9, 3.10, 3.11, 3.12
- **Code Quality Checks:**
  - Flake8 (linting)
  - Black (code formatting)
- **Testing:**
  - Pytest with coverage reporting
  - Coverage uploaded to Codecov
- **Status:** Must pass before other jobs run

#### Train Model
- Depends on: Test Suite (runs after tests pass)
- Downloads training data
- Runs full ML pipeline
- Uploads MLflow artifacts
- Uploads trained models
- **Note:** Gracefully handles missing data with warnings

#### Code Quality Analysis
- Pylint for code analysis
- Bandit for security scanning
- Runs in parallel with other jobs

#### Build Package
- Creates Python distribution packages
- Generates wheel files
- Uploads build artifacts

#### Notify Results
- Final status check
- Aggregates results from all jobs

### 2. Integration Tests Pipeline (`.github/workflows/integration-tests.yml`)

**Triggers:** Push to master/main, Pull Requests

**Purpose:** End-to-end validation
- Creates sample data if needed
- Runs complete pipeline
- Verifies model artifacts
- Tests model loading

## Docker Setup

### Dockerfile
Multi-stage build optimized for production:
- Python 3.11 slim base image
- Minimal dependencies
- Exposes port 5000 for MLflow UI

### Docker Compose
Orchestrates three services:

**mlflow**
- Runs MLflow tracking server
- Exposes UI on port 5000
- Persists data in volumes

**training**
- Runs the full ML pipeline
- Mounts data and model directories
- Depends on mlflow service

**api**
- FastAPI application server
- Exposes API on port 8000
- Loads trained models

## Pre-Commit Hooks

### Setup
```bash
pip install pre-commit
pre-commit install
```

### Hooks Configured
- Trailing whitespace cleaning
- End-of-file fixing
- YAML validation
- Large file detection (>1MB)
- Merge conflict detection
- Private key detection
- Black formatting (line length: 120)
- isort import sorting
- Flake8 linting
- Pylint static analysis

## Local Development

### 1. Install Dependencies
```bash
cd churn_prediction
pip install -r requirements.txt
pip install pre-commit  # For hooks
```

### 2. Setup Pre-Commit
```bash
pre-commit install
pre-commit run --all-files  # Run all checks manually
```

### 3. Run Tests Locally
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### 4. Run Pipeline Manually
```bash
python -c "from src.pipeline.pipeline import run_pipeline; run_pipeline()"
```

### 5. Start MLflow UI
```bash
mlflow ui --host 0.0.0.0
# Visit http://localhost:5000
```

## Docker Workflow

### Build Image
```bash
docker build -t customer-churn:latest .
```

### Run with Docker Compose
```bash
docker-compose up
# MLflow UI: http://localhost:5000
# API: http://localhost:8000
```

### Run Just Training
```bash
docker-compose run training
```

## Configuration

### Environment Variables
Place in `.env` file:
```
MLFLOW_TRACKING_URI=sqlite:///mlflow.db
PYTHONPATH=/app
```

### Config File
Edit `config/config.yaml` to adjust:
- Target column and test size
- Scaler type (standard/minmax)
- SMOTE configuration
- Model hyperparameters
- MLflow experiment settings

## Artifacts

### What Gets Created

**Local Artifacts:**
- `models/model.pkl` - Trained model
- `models/scaler.pkl` - Data scaler
- `mlruns/` - MLflow runs and experiments
- `logs/` - Application logs
- `reports/` - Generated reports

**CI/CD Uploads:**
- Coverage reports to Codecov
- MLflow artifacts (30-day retention)
- Trained models (30-day retention)
- Security scan results (30-day retention)
- Distribution packages (30-day retention)

## Monitoring

### GitHub Actions Dashboard
- View all workflow runs: Go to Actions tab
- Check job logs for debugging
- Download artifacts from completed runs

### MLflow UI
- Track experiments and runs
- Compare model metrics
- View parameters and artifacts
- Access trained models

### Code Coverage
- Codecov integration shows coverage trends
- Coverage reports available in GitHub PRs

## Troubleshooting

### Tests Failing
1. Check Python version compatibility
2. Review test logs in GitHub Actions
3. Run tests locally: `pytest tests/ -v`

### Model Training Failing
1. Verify data file exists
2. Check config.yaml syntax
3. Review MLflow logs

### Docker Issues
1. Ensure Docker is running
2. Check port availability (5000, 8000)
3. Review docker-compose logs: `docker-compose logs -f`

### Pre-Commit Hook Issues
```bash
# Skip hooks (not recommended)
git commit --no-verify

# Update hooks
pre-commit autoupdate

# Debug specific hook
pre-commit run [hook-id] --all-files
```

## Best Practices

1. **Branch Protection**
   - Require status checks before merge
   - Require code reviews

2. **Secrets Management**
   - Never commit `.env` files
   - Use GitHub Secrets for sensitive data

3. **Data Management**
   - Keep training data in `.gitignore`
   - Use data versioning tools (DVC) for large datasets

4. **Model Versioning**
   - Track models in MLflow
   - Use semantic versioning for releases

5. **Documentation**
   - Update README with new features
   - Document configuration changes

## Performance Optimization

### Caching
- GitHub Actions caches pip dependencies
- Docker layer caching for builds

### Parallel Jobs
- Code quality checks run in parallel
- Multiple Python versions tested simultaneously

### Conditional Execution
- Training only runs if tests pass
- Notification job waits for all jobs

## Future Enhancements

1. **Model Deployment**
   - Add AWS/GCP deployment steps
   - Container registry integration

2. **Performance Monitoring**
   - Add model drift detection
   - Performance tracking dashboard

3. **Automated Retraining**
   - Schedule weekly/monthly retraining
   - Trigger on data updates

4. **API Testing**
   - Add integration tests for API endpoints
   - Load testing

5. **Notification**
   - Slack/email alerts on failures
   - Custom dashboards
