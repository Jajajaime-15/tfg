import flet as ft # type: ignore
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
from views.carga import VistaCarga
import asyncio # lo necesitamos para poder ver la carga

async def main(page: ft.Page):
    page.title = "UBIKA"
    page.window_width = 400
    page.window_height = 700

    # cargamos el tema que está guardado
    tema_guardado = await page.shared_preferences.get("tema")
    if tema_guardado == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    
    # mostramos la vista de carga mientras se inicializan los servicios y controladores
    vista_carga = VistaCarga(page)
    page.add(vista_carga.vista())
    page.update()
    await asyncio.sleep(2) # tiempo de espera para que se vea la vista de carga
    
    # arrancamos Firebase
    fb_service = FirebaseService(page)

    # servicios
    auth_service = AuthService(page, fb_service)
    usuario_service = UsuarioService(page, fb_service)
    ajustes_service = AjustesService(page, fb_service)
    gps_service = GPSService(page, fb_service)

    # controladores
    auth_controller = AuthController(page, auth_service)
    ajustes_controller = AjustesController(page, ajustes_service, usuario_service, auth_service)
    usuario_controller = UsuarioController(page, usuario_service)
    mapa_controller = MapaController(page, gps_service)

    # arrancamos el archivo de las rutas y conectamos con la funcion de cambio de ruta del router
    router = Router(page, auth_controller, ajustes_controller, usuario_controller, mapa_controller)
    page.router = router # al cerrar sesion reseteamos el router
    page.on_route_change = router.cambiar_ruta
    page.on_view_pop = router.volver_atras # evento de flet que hace que se ejecute la función de volver atras usando la navegacion del movil


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