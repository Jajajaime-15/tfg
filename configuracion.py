import pyrebase
import os
from dotenv import load_dotenv

# cargar las variables de .env
load_dotenv()

config = {
    "apiKey": os.getenv("FB_API_KEY"),
    "authDomain": "tracking-familiar.firebaseapp.com",
    "databaseURL": "https://tracking-familiar-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "tracking-familiar",
    "storageBucket": "tracking-familiar.firebasestorage.app",
    "messagingSenderId": "425018208271",
    "appId": "1:425018208271:web:044aa2209607b24ffb337a"
}

# Inicializamos Firebase una sola vez
firebase = pyrebase.initialize_app(config)

# Exportamos los servicios para usarlos en otros archivos
auth = firebase.auth()
db = firebase.database()