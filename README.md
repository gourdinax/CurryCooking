# Prédiction des 3 Points de Stephen Curry

Ce projet est une application web qui prédit le nombre de tirs à 3 points que Stephen Curry réalisera dans un match en fonction du nombre de minutes jouées et du nombre de tentatives de tirs à 3 points. L'application utilise FastAPI pour l'API de prédiction et Flask pour l'interface web. Le projet intègre également GPT-3.5 d'OpenAI pour des prédictions supplémentaires.

## Structure du projet


Voici un exemple de fichier README.md pour votre projet en français. Ce fichier présente le projet et fournit des instructions détaillées sur la façon de le configurer et de le faire fonctionner.

README.md
markdown
Copier le code
# Prédiction des 3 Points de Stephen Curry

Ce projet est une application web qui prédit le nombre de tirs à 3 points que Stephen Curry réalisera dans un match en fonction du nombre de minutes jouées et du nombre de tentatives de tirs à 3 points. L'application utilise FastAPI pour l'API de prédiction et Flask pour l'interface web. Le projet intègre également GPT-3.5 d'OpenAI pour des prédictions supplémentaires.

## Structure du projet

curryCooking/
├── pycache/
├── models/
├── static/
├── templates/
│ ├── index.html
│ ├── results.html
├── .env
├── .gitignore
├── app.py
├── Basket_Stephen_Curry_Axel_Gourdin_Abdoula_Jaiteh_William_Girard-Reydet.ipynb
├── fastapi_app.py
├── flask_app.py
├── functions.py
├── README.md
├── requirements.txt
└── Stephen_Curry_Stats.csv


## Fonctionnalités

- **FastAPI** : Fournit des points de terminaison API pour l'entraînement et la prédiction des modèles.
- **Flask** : Sert l'interface web pour les interactions utilisateur.
- **OpenAI GPT-3.5** : Fournit des prédictions supplémentaires à l'aide d'un modèle d'IA conversationnel.
- **Gestion des modèles** : Stocke et gère plusieurs versions des modèles entraînés.

## Prérequis

- Python 3.8+
- pip

## Installation

```bash
git clone https://github.com/gourdinax/CurryCooking.git
cd curryCooking

#Créez un environnement virtuel et activez-le :
python -m venv venv
source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`

#Installez les dépendances requises :
pip install -r requirements.txt

#Créez un fichier .env dans le répertoire racine et ajoutez votre clé API OpenAI :
OPENAI_API_KEY=votre_cle_api_openai_ici

#Démarrez les applications FastAPI et Flask :
python app.py

#Ouvrez votre navigateur web et allez à http://127.0.0.1:5000 pour accéder à l'interface web.
```

# Points de terminaison

## FastAPI :

POST /predict_future : Prédire le nombre de tirs à 3 points.
POST /train_model : Entraîner un nouveau modèle avec un fichier CSV.
GET /model : Obtenir des prédictions à l'aide du modèle local et d'OpenAI.

## Flask :

/ : Page principale avec des formulaires pour les prédictions et l'entraînement des modèles.

# Entraîner un nouveau modèle

Préparez un fichier CSV avec les colonnes identiques à celle dans le fichier Stephen_Curry_Stats.csv.
Utilisez l'interface web pour télécharger le fichier CSV et entraîner un nouveau modèle. 
Le nouveau modèle sera stocké et utilisé pour les prédictions suivantes.

Projet réalisé par : 

-   Axel Gourdin
-   Abdoula Jaiteh
-   William Girard-Reydet









