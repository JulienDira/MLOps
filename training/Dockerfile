# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système requises par scikit-learn
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY train.py .
COPY api_train.py .

# MLflow will store data here locally
RUN mkdir -p /mlruns

CMD ["uvicorn", "api_train:app", "--host", "0.0.0.0", "--port", "4000"]