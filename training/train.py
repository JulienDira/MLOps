import mlflow
import mlflow.sklearn
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import argparse

# Configuration des arguments
parser = argparse.ArgumentParser()
parser.add_argument("--test_size", type=float, default=0.2)
parser.add_argument("--n_estimators", type=int, default=100)
parser.add_argument("--max_depth", type=int, default=10)
parser.add_argument("--random_state", type=int, default=42)
args = parser.parse_args()

# Chargement des données
data = fetch_california_housing()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split avec paramètre dynamique
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=args.test_size, 
    random_state=42
)

with mlflow.start_run():
    
    # Log des paramètres dynamiques
    mlflow.log_params({
        "test_size": args.test_size,
        "n_estimators": args.n_estimators,
        "max_depth": args.max_depth,
        "random_state": args.random_state
    })

    # Entraînement du modèle
    model = RandomForestRegressor(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        random_state=args.random_state
    )
    
    model.fit(X_train, y_train)

    # Prédictions
    predictions = model.predict(X_test)

    # Évaluation
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    # Log des métriques
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    # Exemple d'entrée pour signature
    input_example = X_test.iloc[:1]

    # Log du modèle avec signature
    mlflow.sklearn.log_model(
        sk_model=model,
        name="random_forest_model",
        input_example=input_example,
        registered_model_name="RandomForestRegressorByRakuzanModel" 
    )

    print(f"📊 MSE: {mse:.3f} | RMSE: {rmse:.3f} | R2: {r2:.3f}")
    print("✅ Modèle RandomForest enregistré dans MLflow.")
    
    run_id = mlflow.active_run().info.run_id
    print(f"MLflow Run ID: {run_id}")  # Critical pour l'API
