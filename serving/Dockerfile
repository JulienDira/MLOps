FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models /models

EXPOSE 5001

# 🔥 Ajout de --no-conda pour éviter pyenv/conda
CMD ["mlflow", "models", "serve", "-m", "/models", "--host", "0.0.0.0", "--port", "5001", "--no-conda"]