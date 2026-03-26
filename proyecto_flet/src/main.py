import flet as ft
from database.wrapper import Wrapper
from controllers.auth_controller import AuthController
from router import Router

async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_100)
    page.title = "Login"
    page.window_width = 400
    page.window_height = 700
    
    # Inicializamos la base de datos y el controlador
    wrapper = Wrapper(page)
    controlador_auth = AuthController(page, wrapper)
    
    # Instanciamos el router pasándole el page y el controlador 
    my_router = Router(page, controlador_auth)
    
    # Cuando la ruta cambie, se llamara a my_router.route_change
    page.on_route_change = my_router.route_change
    
    # Arrancamos en la ruta actual
    await my_router.route_change(None)

ft.app(target=main)