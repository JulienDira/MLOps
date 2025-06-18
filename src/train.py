import mlflow
import mlflow.sklearn
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd

# Charger les données
data = fetch_california_housing()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Afficher un aperçu du dataset
print("📊 Aperçu des données :")
print(X.head())
print("\n🎯 Aperçu de la cible :")
print(y[:5])

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparamètres
n_estimators = 100
max_depth = 10
random_state = 42

# MLflow run
with mlflow.start_run(run_name="RandomForestRegressor") as run:

    # Log des hyperparamètres
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # Entraînement du modèle
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
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
