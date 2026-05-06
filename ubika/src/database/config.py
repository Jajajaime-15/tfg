import os
from dotenv import load_dotenv 

load_dotenv() # carga el archivo .env

# configuración de firebase cogiendo los datos de .env
config = {
    "apiKey": os.getenv("FB_API_KEY"),
    "authDomain": os.getenv("FB_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FB_DATABASE_URL"),
    "projectId": os.getenv("FB_PROJECT_ID"),
    "storageBucket": os.getenv("FB_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FB_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FB_APP_ID")
}
