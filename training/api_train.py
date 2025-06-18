from fastapi import FastAPI, HTTPException
import subprocess
import mlflow
import uvicorn
import logging
from pydantic import BaseModel

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class TrainRequest(BaseModel):
    test_size: float = 0.2
    n_estimators: int = 100
    max_depth: int = 10
    
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/train")
def train_model(params: TrainRequest):
    try:
        logger.info(f"Début entraînement avec params: {params}")
        
        # 1. Exécution avec vérification des erreurs
        result = subprocess.run(
            [
                "python", "train.py",
                "--test_size", str(params.test_size),
                "--n_estimators", str(params.n_estimators),
                "--max_depth", str(params.max_depth),
                "--random_state", "42"
            ],
            capture_output=True,
            text=True,
            check=True  # Lève une exception si échec
        )
        
        # 2. Parsing du run_id depuis les logs
        run_id = None
        for line in result.stdout.split('\n'):
            if "MLflow Run ID:" in line:
                run_id = line.split(":")[1].strip()
                break
                
        if not run_id:
            raise ValueError("Run ID non trouvé dans les logs")

        return {"status": "success", "run_id": run_id}
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Erreur dans train.py:\n{e.stderr}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
        
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)