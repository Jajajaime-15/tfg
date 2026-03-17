import flet as ft # para flet
import pyrebase # para firebase
import flet_geolocator as ftg # para la geolocalizacion
import flet_map as ftm # para el mapa
from db.config import config_keys # las claves que tenemos en el .env

firebase = pyrebase.initialize_app(config_keys) # iniciamos firebase
db = firebase.database() # instanciamos la base de datos y la autenticacion
auth = firebase.auth()

def main(page: ft.Page):
    print("Firebase conectado")
    page.add(ft.Text("Firebase conectado"))

ft.run(main)