import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Configuration
load_dotenv()
API_URL = os.getenv("MODEL_CHECK_URI", "http://localhost:4000/health")
st.set_page_config(page_title="ML App", layout="wide")

# Vérification de la connexion à l'API
def check_api_health():
    try:
        response = requests.get(f"{API_URL}", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Page d'accueil
st.title("🤖 Application de Machine Learning")

if not check_api_health():
    st.error("⚠️ L'API n'est pas disponible. Veuillez démarrer le service API.")
    st.stop()

st.success("✅ Connecté à l'API")