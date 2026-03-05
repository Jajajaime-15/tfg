import flet as ft
import pyrebase
import os
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__)) # ruta de la carpeta actual (ruta del script)
dotenv_path = os.path.join(script_dir, '..', '.env') # Creamos la ruta subiendo un nivel para buscar el archivo .env en la carpeta raíz
load_dotenv(dotenv_path) # cargamos el .env

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
        mensaje.value=f"Error: {e}"
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
        mensaje.value=f"Error al iniciar sesión: {e}"
        mensaje.color="red"
    page.update()

# parte de Flet (app)
def main(page: ft.Page):
    #configurar la ventana
    page.title="Pruebas 10 de marzo Alba"
    page.window_width=400
    page.window_height=700
    page.bgcolor="#F0F2F5"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #contenido de la ventana
    icono = ft.Icon(icon=ft.Icons.LOCK, size=80, color="blue")
    titulo = ft.Text("Control familiar",size=25,weight="blue")
    subtitulo = ft.Text("Inicia sesión",size=16, color="grey")
    email_usu = ft.TextField(label="Email",width=300)
    psw_usu = ft.TextField(label="Constraseña", password=True, can_reveal_password=True, width=300)
    resultado = ft.Text(size=14, weight="w500")
    
    btn_iniciar = ft.FilledButton(
        "Iniciar Sesión",width=340, height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
        on_click=lambda _: iniciar_sesion(email_usu,psw_usu,resultado,page)
    )
    btn_crear = ft.FilledButton(
        "Nueva cuenta",
        on_click=lambda _: crear_usuario(email_usu,psw_usu,resultado,page)
    )

    # creamos el container para personalizarlo
    contenedor = ft.Container(
        # columna en la que colocamos todo
        content=ft.Column([icono,
                titulo,
                subtitulo,
                ft.Divider(height=20, color="transparent"), # divisor para separar los campos
                email_usu,
                psw_usu,
                ft.Divider(height=10, color="transparent"),
                btn_iniciar,
                btn_crear,
                resultado,],
                # alineamos y damos espacio en la columna
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
                ),
                # formato del contenedor, color de fondo, espacio, borde, sombra...
                bgcolor="white",
                padding=40,
                border_radius=30,
                shadow=ft.BoxShadow(
                    blur_radius=20, 
                    color="#20000000",
                    spread_radius=1
                ),
                width=400,
    )
    #agregar el contenido a la ventana
    page.add(contenedor)

# iniciar app
ft.app(target=main, view=ft.AppView.WEB_BROWSER) #para evitar problemas a la hora de abrir se pone WB_BROWSER para que abra una pestaña en el navegador
