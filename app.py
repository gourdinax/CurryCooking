from threading import Thread
import uvicorn

# Importer les applications Flask et FastAPI
from flask_app import flask_app
from fastapi_app import app as fastapi_app

def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8001)  # Utiliser un port différent pour FastAPI

if __name__ == "__main__":
    # Démarrer FastAPI dans un thread séparé
    fastapi_thread = Thread(target=run_fastapi)
    fastapi_thread.start()
    
    # Démarrer l'application Flask
    flask_app.run(port=5000)
