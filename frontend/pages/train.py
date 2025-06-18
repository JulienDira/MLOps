import streamlit as st
import requests
import os

st.title("🏋️ Entraînement MLflow")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_SERVING_URI = os.getenv("MODEL_SERVING_URI", "http://localhost:5001/invocations")
MODEL_TRAIN_URI = os.getenv("MODEL_TRAIN_URI", "http://localhost:4000/train")

# Paramètres d'entraînement
with st.form("train_params"):
    st.header("Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        test_size = st.slider("Test Size", 0.1, 0.5, 0.2, 0.05)
        n_estimators = st.number_input("n_estimators", 50, 500, 100)
    
    with col2:
        max_depth = st.number_input("max_depth", 3, 50, 10)
    
    if st.form_submit_button("Lancer l'entraînement"):
        try:
            response = requests.post(
                "http://mlflow-train:4000/train",
                json={
                    "test_size": test_size,
                    "n_estimators": n_estimators,
                    "max_depth": max_depth
                },
                timeout=300
            )
            
            if response.status_code == 200:
                st.success("Entraînement réussi!")
                run_id = response.json()["run_id"]
                st.markdown(f"**Run ID:** `{run_id}`")
                
                st.link_button(
                    "Voir dans MLflow UI",
                    f"{MLFLOW_TRACKING_URI}/#/experiments/0/runs/{run_id}"
                )
            else:
                st.error(f"Erreur: {response.text}")
                
        except Exception as e:
            st.error(f"Erreur de connexion: {str(e)}")