from dotenv import load_dotenv # para cargar el .env
import os

load_dotenv()

# las claves que tenemos en el .env
config_keys = {
    "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyDHAmnQwPIgAwXL9HdJbAvI1mMJ_b75SII"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "prueba02-47c48.firebaseapp.com"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "https://prueba02-47c48-default-rtdb.europe-west1.firebasedatabase.app/"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID", "prueba02-47c48"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "prueba02-47c48.firebasestorage.app"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "751302808767"),
    "appId": os.getenv("FIREBASE_APP_ID", "1:751302808767:web:293bbb2cb20a241f83220a")
}