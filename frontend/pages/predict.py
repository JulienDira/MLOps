import streamlit as st
import requests
import pandas as pd
import os

# Configuration
st.set_page_config(page_title="🔮 Prédiction MLflow", layout="wide")

# Variables d'environnement (à définir dans docker-compose ou .env)
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000")
MODEL_SERVING_URI = os.getenv("MODEL_SERVING_URI", "http://mlflow-model-serving:5001/invocations")
MODEL_NAME = "RandomForestRegressorByRakuzanModel"  # Nom donné dans mlflow.log_model()

st.title("🔮 Prédiction via MLflow API")

# 1. Vérification du modèle disponible
try:
    # Récupère la dernière version du modèle
    model_status = requests.get(
        f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/registered-models/get-latest-versions",
        params={"name": MODEL_NAME}
    )
    
    if model_status.status_code != 200:
        st.warning("Aucun modèle disponible. Veuillez d'abord entraîner un modèle.")
        st.stop()
    else:
        latest_version = model_status.json()["model_versions"][0]
        st.success(f"Modèle chargé : {MODEL_NAME} (version {latest_version['version']})")
        
except requests.exceptions.RequestException:
    st.error("Impossible de se connecter au serveur MLflow")
    st.stop()

# 2. Formulaire de prédiction
st.header("Saisie des caractéristiques")

# Features du modèle California Housing (adaptez selon votre modèle)
feature_columns = [
    "MedInc", "HouseAge", "AveRooms", 
    "AveBedrms", "Population", "AveOccup", 
    "Latitude", "Longitude"
]

inputs = {}
cols = st.columns(2)

for i, feature in enumerate(feature_columns):
    with cols[i % 2]:
        # Valeurs par défaut réalistes pour démo
        default_val = 3.0 if "Ave" in feature else 150.0 if feature == "Population" else 35.0 if feature == "HouseAge" else -120.0 if feature == "Longitude" else 8.0
        inputs[feature] = st.number_input(feature, value=default_val, step=0.1)

# 3. Bouton de prédiction
if st.button("Effectuer la prédiction", type="primary"):
    try:
        # Formatage pour MLflow (dataframe_split)
        payload = {
            "dataframe_split": {
                "columns": feature_columns,
                "data": [list(inputs.values())]
            }
        }
        
        response = requests.post(
            MODEL_SERVING_URI,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Valeur prédite : ${prediction['predictions'][0]:.2f}K")  # Format $
            
            # Optionnel : Affichage des features importance si disponible
            st.subheader("Influence des caractéristiques")
            importance_df = pd.DataFrame({
                "Feature": feature_columns,
                "Importance": [abs(val) for val in inputs.values()]  # Exemple simplifié
            }).sort_values("Importance", ascending=False)
            
            st.bar_chart(importance_df.set_index("Feature"))
            
        else:
            st.error(f"Erreur du modèle : {response.text}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API : {str(e)}")