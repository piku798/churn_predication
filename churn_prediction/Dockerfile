FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY churn_prediction/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY churn_prediction/ .

# Create necessary directories
RUN mkdir -p models logs data/raw data/processed mlruns

# Expose MLflow UI port
EXPOSE 5000

# Default command runs MLflow UI
CMD ["mlflow", "ui", "--host", "0.0.0.0"]
