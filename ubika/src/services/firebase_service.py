import pyrebase # para firebase en python
from database.config import config # las claves que tenemos en el .env

class FirebaseService:
    def __init__(self, page):
        self.page = page
        try:
            self.firebase = pyrebase.initialize_app(config)
            self.auth = self.firebase.auth()
            self.db = self.firebase.database()
            self.id_usuario = None
            self.token = None
            print("Conectado a firebase") # print para comprobar que no hay problema a la hora de conectarse
        except Exception as e:
            print(f"Error al conectarse a firebase: {e}")