import flet as ft
from services.grupo_service import Wrapper as WrapperGrupo
from services.usuario_service import Wrapper as WrapperUsuario
from controllers.user_controller import UserController
from router import Router

async def main(page: ft.Page):
    page.title = "PROYECTO TFG"
    page.window_width = 400
    page.window_height = 700
    page.bgcolor = "white"

    # arrancamos Firebase
    wrapper_grupos = WrapperGrupo(page)
    await wrapper_grupos.cargar_datos_usuario()
    wrapper_usuarios = WrapperUsuario(page)
    user_controller = UserController(page,wrapper_usuarios)

    # Cerramos la sesión al arrancar para que siempre aparezca el login SOLO PARA PRUEBAS
    #await wrapper.cerrar_sesion() 
    # o limpiamos los datos guardados en el dispositivo
    #await page.shared_preferences.clear()
    
    # arrancamos el archivo de las rutas
    router = Router(page,wrapper_usuarios, wrapper_grupos)
    # conectamos con la funcion de cambio de ruta del router (route_change)
    page.on_route_change = router.route_change

    # comprobamos si hay un usuario logueado ya
    id_usuario = await wrapper_usuarios.usuario_conectado()
    if id_usuario:
        print("USUARIO INICIADO") # PRINT PARA PROBAR QUE SE QUEDA INICIADA LA SESION
        page.route = "/" # esta ruta será la de grupos
    else:
        page.route = "/" # ruta de login (principal)

    await router.route_change(None) # cargamos la primera vista
    page.update()

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER,assets_dir="../assets")