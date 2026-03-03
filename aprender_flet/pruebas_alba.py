import flet as ft
import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

# datos de firebase
config = {
  "apiKey": os.getenv("FB_API_KEY"),
  "authDomain": "tracking-familiar.firebaseapp.com",
  "projectId": "tracking-familiar",
  "storageBucket": "tracking-familiar.firebasestorage.app",
  "messagingSenderId": "425018208271",
  "appId": "1:425018208271:web:044aa2209607b24ffb337a",
  "databaseURL": ""
}

# iniciar firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# funciones de crear un usuario e iniciar sesion con un usuario
def crear_usuario(email_text,psw_text,mensaje,page):
    try:
        email=email_text.value
        psw=psw_text.value
        auth.create_user_with_email_and_password(email,psw)
        mensaje.value="Se ha creado el usuario en Firebase"
        mensaje.color="green" #color en el que aparece el mensaje de creacion
        email_text.value=""
        psw_text.value=""
    except Exception as e:
        mensaje.value="Error: {e}"
        mensaje.color="red" #color en el que aparece el mensaje de error
    page.update()

def iniciar_sesion(email_text,psw_text,mensaje,page):
    try:
        email=email_text.value
        psw=psw_text.value
        auth.sign_in_with_email_and_password(email,psw)
        mensaje.value="Sesión iniciada"
        mensaje.color="green"
        email_text.value=""
        psw_text.value=""
    except Exception as e:
        mensaje.value="Error al iniciar sesión"
        mensaje.color="red"
    page.update()

# parte de Flet (app)
def main(page: ft.Page):
    #configurar la ventana
    page.title="Pruebas 10 de marzo Alba"
    page.window_width=400
    page.window_height=500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #contenido de la ventana
    titulo = ft.Text("Iniciar sesión",size=25,weight="bold")
    email_usu = ft.TextField(label="Email",width=300)
    psw_usu = ft.TextField(label="Constraseña", password=True, can_reveal_password=True, width=300)
    resultado = ft.Text()
    
    btn_iniciar = ft.FilledButton(
        "Iniciar Sesión",
        on_click=lambda _: iniciar_sesion(email_usu,psw_usu,resultado,page)
    )
    btn_crear = ft.FilledButton(
        "Nueva cuenta",
        on_click=lambda _: crear_usuario(email_usu,psw_usu,resultado,page)
    )

    #agregar el contenido a la ventana
    page.add(
        ft.Column(
            [titulo,email_usu,psw_usu,btn_crear,btn_iniciar,resultado],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

# iniciar app
ft.app(target=main, view=ft.AppView.WEB_BROWSER) #para evitar problemas a la hora de abrir se pone WB_BROWSER para que abra una pestaña en el navegador
