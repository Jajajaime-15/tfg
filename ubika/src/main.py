import flet as ft
from services.ajustes_service import AjustesService
from services.auth_service import AuthService
from services.firebase_service import FirebaseService
from services.usuario_service import UsuarioService
from services.gps_service import GPSService
from controllers.auth_controller import AuthController
from controllers.usuario_controller import UsuarioController
from controllers.ajustes_controller import AjustesController
from controllers.mapa_controller import MapaController
from router import Router

async def main(page: ft.Page):
    page.title = "UBIKA"
    page.window_width = 400
    page.window_height = 700
    
    # funcion para el boton de volver atras de la barra de navegación del movil
    async def volver_atras(e):
        e.prevent_default = True # con esto bloqueamos a que flet haga el pop automático por su cuenta y se oblique ha hacer según se indique en nuestro route
        # de registro > perfil
        if page.route == "/registro":
            page.route = "/"
            await page.push_route("/") 
            return
        # de ajustes > login
        if page.route == "/settings":
            page.route = "/home"
            await page.push_route("/home")
            return 
        # de Vista Principal (Grupos, Mapa o Perfil) > minimizamos la aplicacion
        if page.route == "/home":
            return 
        # de login > minimizamos la aplicacion
        if page.route == "/":
            return

    page.on_view_pop = volver_atras # evento de flet que hace que se ejecute la función de volver atras usando la navegacion del movil

    # cargamos el tema que está guardado
    tema_guardado = await page.shared_preferences.get("tema")
    if tema_guardado == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
        
    # arrancamos Firebase
    fb_service = FirebaseService(page)

    # servicios
    auth_service = AuthService(page, fb_service)
    usuario_service = UsuarioService(page, fb_service, auth_service)
    ajustes_service = AjustesService(page, fb_service, auth_service)
    gps_service = GPSService(page, fb_service)

    # controladores
    auth_controller = AuthController(page, auth_service)
    ajustes_controller = AjustesController(page, ajustes_service, usuario_service, None)
    usuario_controller = UsuarioController(page, usuario_service, ajustes_controller)
    mapa_controller = MapaController(page, gps_service)

    # arrancamos el archivo de las rutas y conectamos con la funcion de cambio de ruta del router
    router = Router(page, auth_controller, ajustes_controller, usuario_controller, mapa_controller)
    ajustes_controller.router = router # al cerrar sesion reseteamos el router
    page.on_route_change = router.cambiar_ruta 

    # comprobamos si hay algun usuario que haya iniciado sesion ya
    id_usuario = await auth_service.usuario_conectado()
    if id_usuario:
        usuario_service.id_usuario = id_usuario
        usuario_service.token = auth_service.token
        await usuario_service.sincronizar() # sincronizamos con firebase
        page.route = "/home" # ruta principal que carga los grupos
    else:
        page.route = "/" # ruta de login
        
    await router.cambiar_ruta(None) # cargamos la primera vista
    page.update()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")