import flet as ft # type: ignore
from services.ajustes_service import AjustesService
from services.auth_service import AuthService
from services.firebase_service import FirebaseService
from services.usuario_service import UsuarioService
from controllers.auth_controller import AuthController
from controllers.usuario_controller import UserController
from controllers.ajustes_controller import SettingsController
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
    fb_service = FirebaseService(page)
    auth_service = AuthService(page, fb_service)
    usuario_service = UsuarioService(page, fb_service, auth_service)
    ajustes_service = AjustesService(page, fb_service, auth_service)
    auth_controller = AuthController(page,auth_service)
    ajustes_controller = SettingsController(page,ajustes_service)
    usuario_controller = UserController(page,usuario_service)

    # Cerramos la sesión al arrancar para que siempre aparezca el login SOLO PARA PRUEBAS
    # await wrapper.cerrar_sesion() 
    # o limpiamos los datos guardados en el dispositivo
    # await page.shared_preferences.clear()
    
    # arrancamos el archivo de las rutas
    router = Router(page,auth_controller,ajustes_controller,usuario_controller)
    # conectamos con la funcion de cambio de ruta del router (route_change)
    page.on_route_change = router.route_change

    # comprobamos si hay un usuario logueado ya
    id_usuario = await auth_service.usuario_conectado()
    if id_usuario:
        print("USUARIO INICIADO") # PRINT PARA PROBAR QUE SE QUEDA INICIADA LA SESION
        page.route = "/home" # esta ruta será la de grupos
    else:
        page.route = "/" # ruta de login (principal)
        
    await router.route_change(None) # cargamos la primera vista
    page.update()

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER,assets_dir="assets")