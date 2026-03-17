import flet as ft
from database.wrapper import Wrapper
from controllers.auth_controller import AuthController

async def main(page: ft.Page):
    wrapper = Wrapper(page)
    auth_doc = AuthController(page, wrapper)

    nombre = ft.TextField(label="Nombre")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Password", password=True)
    telefono = ft.TextField(label="Teléfono")
    mensaje = ft.Text(value="", color="red")

    async def on_registro(e):
        await auth_doc.registrarse(nombre, email, password, telefono, mensaje)

    async def on_login(e):
        await auth_doc.conectarse(email, password, mensaje)

    async def on_cerrar(e):
        await wrapper.cerrar_sesion()

    # Comprobar si ya hay sesión al arrancar
    id_guardado = await wrapper.usuario_conectado()
    if id_guardado:
        print(f"Sesión restaurada: {id_guardado}")
        page.push_route("/home")  # ajusta la ruta a la tuya

    page.add(
        ft.Text("PRUEBAS ALBA", size=20, weight="bold"),
        nombre, email, password, telefono,
        mensaje,
        ft.Row([
            ft.Button("Probar Registro", on_click=on_registro),
            ft.Button("Probar Login", on_click=on_login),
        ]),
        ft.Divider(),
        ft.Button("Cerrar Sesión", on_click=on_cerrar)
    )

ft.run(main)