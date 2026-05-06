import flet as ft
from views.login_view import VistaLogin
from views.registro_view import VistaRegistro
from views.principal_view import VistaPrincipal
from views.ajustes_view import VistaAjustes

class Router:
    def __init__(self, page, controlador_auth, controlador_settings, controlador_user, controlador_mapa):
        self.page = page
        self.controlador_auth = controlador_auth
        self.controlador_settings = controlador_settings
        self.controlador_user = controlador_user
        self.controlador_mapa = controlador_mapa
        self.vista_principal = None
        
        # Diccionario de rutas con sus controladores correspondientes
        self.routes = {
            "/": (VistaLogin, controlador_auth), # vista iniciar sesión (Alba)
            "/registro": (VistaRegistro, controlador_auth), # vista registrarse (Alba)
            "/settings": (VistaAjustes, controlador_settings), # vista ajustes (Alba)
            "/home": (VistaPrincipal,(controlador_user, controlador_mapa)) # vista principal después de hacer login con grupos (Julio)
        }

    # funcion para evitar que si se cierra sesion y se abre con otro usuario no nos cargue los datos del anterior (se usa en cerrar sesion)
    def reset_vistas(self):
        self.vista_principal = None
        
    async def cambiar_ruta(self, e):
        print(f"Cambiando a la ruta: {self.page.route}")

        # definimos la pila segun la ruta
        pila = {
            "/settings": ["/home", "/settings"],
            "/home": ["/home"],
            "/registro": ["/", "/registro"]
        }
        pila_rutas = pila.get(self.page.route, ["/"])

        # reconstruimos la pila de las vistas
        self.page.views.clear()
        for ruta in pila_rutas:
            vista_clase, controlador = self.routes[ruta]
            
            if vista_clase == VistaPrincipal:
                if not self.vista_principal:
                    self.vista_principal = VistaPrincipal(self.page, controlador[0], controlador[1])
                pantalla = self.vista_principal
            else:
                pantalla = vista_clase(self.page, controlador)
                if vista_clase == VistaLogin or vista_clase == VistaRegistro:
                    self.controlador_auth.vista = pantalla
                if vista_clase == VistaAjustes: 
                    self.controlador_settings.vista = pantalla
            # creamos la vista física y la añadimos a la pila de navegación para mostrarla
            self.page.views.append(ft.View(route=ruta, controls=[pantalla.vista()], padding=0))

        self.page.update()

        if self.page.route == "/home":
            await self.controlador_user.service.sincronizar()
            if self.controlador_mapa.geo:
                await self.controlador_mapa.iniciar_gps()
            else:
                self.page.run_task(self.controlador_mapa.iniciar_gps)
        elif self.page.route == "/settings":
            await self.controlador_settings.cargar_ajustes()
