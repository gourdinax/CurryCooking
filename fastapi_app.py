from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os
import glob
from datetime import datetime
from dotenv import load_dotenv
import openai

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Obtenir la clé API d'OpenAI à partir des variables d'environnement
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key is not set in the environment variables.")

openai.api_key = openai_api_key

app = FastAPI()

# Répertoire pour stocker les modèles
MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

def get_latest_model():
    model_files = glob.glob(f'{MODEL_DIR}/*.pkl')
    if not model_files:
        return None
    latest_model = max(model_files, key=os.path.getctime)
    return joblib.load(latest_model)

# Charger le modèle le plus récent si disponible
model = get_latest_model()

# Charger les données pour obtenir les features
df = pd.read_csv('Stephen_Curry_Stats.csv', sep=';')
df['Dates'] = pd.to_datetime(df['Dates'])
df['Year'] = df['Dates'].dt.year  # Ajouter une colonne Year
df = pd.get_dummies(df, columns=['Opponent'])  # Convertir la colonne 'Opponent' en variables indicatrices
opponent_columns = [col for col in df.columns if col.startswith('Opponent_')]

class FutureMatchRequest(BaseModel):
    minutes: float
    three_point_attempts: float
    opponent: str

@app.post("/predict_future")
def predict_future(request: FutureMatchRequest):
    global model
    if model is None:
        raise HTTPException(status_code=400, detail="Model not trained yet.")
    
    # Préparer les données pour la prédiction
    opponent_encoded = [1 if f'Opponent_{request.opponent}' == col else 0 for col in opponent_columns]
    features = [[request.minutes, request.three_point_attempts] + opponent_encoded]
    
    # Faire la prédiction
    prediction = model.predict(features)
    prediction_rounded = int(np.round(prediction[0]))  # Convertir en type natif
    
    return {"predicted_3_points_successful": prediction_rounded}

@app.post("/train_model")
async def train_model(file: UploadFile = File(...)):
    global model, opponent_columns
    try:
        # Lire le fichier CSV
        df = pd.read_csv(file.file, sep=';')
        
        # Vérifier que les colonnes nécessaires sont présentes
        required_columns = {'Dates', 'Minutes', 'Total 3 Points', '3 Points Succesful', 'Opponent'}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            raise ValueError(f"Missing columns in uploaded file: {missing_cols}")

        df['Dates'] = pd.to_datetime(df['Dates'])
        df['Year'] = df['Dates'].dt.year
        df = pd.get_dummies(df, columns=['Opponent'])
        
        # Préparer les données
        opponent_columns = [col for col in df.columns if col.startswith('Opponent_')]
        X = df[['Minutes', 'Total 3 Points'] + opponent_columns]
        y = df['3 Points Succesful']
        
        # Diviser les données en ensembles d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Entraîner un modèle de forêts aléatoires
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Sauvegarder le modèle avec un nom unique basé sur la date et l'heure
        model_filename = os.path.join(MODEL_DIR, f'rf_model_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pkl')
        joblib.dump(model, model_filename)
        
        # Mettre à jour le modèle courant
        model = get_latest_model()
        
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/model")
def get_model_prediction(minutes: float, three_point_attempts: float, opponent: str):
    # Obtenir la prédiction du modèle local
    opponent_encoded = [1 if f'Opponent_{opponent}' == col else 0 for col in opponent_columns]
    features = [[minutes, three_point_attempts] + opponent_encoded]
    local_prediction = model.predict(features)
    local_prediction_rounded = int(np.round(local_prediction[0]))

    # Obtenir la prédiction de l'API OpenAI
    prompt = f"Combien de 3 points va marquer Stephen Curry en jouant {minutes} minutes avec {three_point_attempts} tirs à 3 points contre {opponent} ? Fait une prédiction."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en prédiction de performances sportives. Répond uniquement à la question posée."},
                {"role": "user", "content": prompt}
            ]
        )
        openai_prediction = response.choices[0]['message']['content']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "local_prediction": local_prediction_rounded,
        "openai_prediction": openai_prediction
    }
