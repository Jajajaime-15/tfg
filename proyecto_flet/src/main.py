import flet as ft # type: ignore
from services.wrapper import Wrapper
from controllers.auth_controller import AuthController
from controllers.user_controller import UserController
from controllers.settings_controller import SettingsController
from router import Router

async def main(page: ft.Page):
    page.title = "PROYECTO TFG"
    page.window_width = 400
    page.window_height = 700
    
    # cargamos el tema que está guardado
    tema_guardado = await page.shared_preferences.get("tema")
    if tema_guardado == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
        
    # arrancamos Firebase
    wrapper = Wrapper(page)
    auth_controller = AuthController(page,wrapper)
    settings_controller = SettingsController(page,wrapper)
    user_controller = UserController(page,wrapper)

    # Cerramos la sesión al arrancar para que siempre aparezca el login SOLO PARA PRUEBAS
    # await wrapper.cerrar_sesion() 
    # o limpiamos los datos guardados en el dispositivo
    # await page.shared_preferences.clear()
    
    # arrancamos el archivo de las rutas
    router = Router(page,auth_controller,settings_controller,user_controller)
    # conectamos con la funcion de cambio de ruta del router (route_change)
    page.on_route_change = router.route_change

    # comprobamos si hay un usuario logueado ya
    id_usuario = await wrapper.usuario_conectado()
    if id_usuario:
        print("USUARIO INICIADO") # PRINT PARA PROBAR QUE SE QUEDA INICIADA LA SESION
        page.route = "/home" # esta ruta será la de grupos
    else:
        page.route = "/" # ruta de login (principal)
        
    await router.route_change(None) # cargamos la primera vista
    page.update()

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER,assets_dir="assets")