import flet as ft
from views.login_view import VistaLogin
from views.registro_view import VistaRegistro
from views.principal_view import VistaPrincipal
from views.ajustes_view import VistaAjustes
from views.crear_grupo_view import VistaCrearGrupo

class Router:
    def __init__(self, page, controlador_auth, controlador_ajustes, controlador_usuario, controlador_mapa, controlador_grupos):
        self.page = page
        self.controlador_auth = controlador_auth
        self.controlador_ajustes = controlador_ajustes
        self.controlador_usuario = controlador_usuario
        self.controlador_mapa = controlador_mapa
        self.controlador_grupos = controlador_grupos
        self.vista_principal = None
        
        # Diccionario de rutas con sus controladores correspondientes
        self.routes = {
            "/": (VistaLogin, controlador_auth),
            "/registro": (VistaRegistro, controlador_auth),
            "/ajustes": (VistaAjustes, controlador_ajustes),
            "/crear_grupo": (VistaCrearGrupo, controlador_grupos), # pasamos el controlador de grupos a la vista de crear grupo para poder usar sus funciones
            "/home": (VistaPrincipal, (controlador_usuario, controlador_mapa, controlador_grupos)) # vista principal después de hacer login con grupos
        }

    # funcion para el boton de volver atras de la barra de navegación del movil
    async def volver_atras(self, e):
        e.prevent_default = True # con esto bloqueamos a que flet haga el pop automático por su cuenta y se oblique ha hacer según se indique en nuestro route
        if self.page.route == "/registro": # de registro > perfil
            self.page.route = "/"
            await self.page.push_route("/")
            return
        if self.page.route == "/ajustes": # de ajustes > login
            self.page.route = "/home"
            await self.page.push_route("/home")
            return 
        if self.page.route == "/home": # de Vista Principal (Grupos, Mapa o Perfil) > minimizamos la aplicacion
            return 
        if self.page.route == "/": # de login > minimizamos la aplicacion
            return

    # funcion para evitar que si se cierra sesion y se inicie de nuevo con otro usuario no nos cargue los datos del anterior
    def reset_vistas(self):
        self.vista_principal = None
        self.controlador_mapa.geo = None
        
    async def cambiar_ruta(self, e):
        if self.page.route == "/home":
            self.reset_vistas()

        pila = { # definimos la pila segun la ruta para asegurar "el volver atrás"
            "/ajustes": ["/home", "/ajustes"],
            "/home": ["/home"],
            "/registro": ["/", "/registro"],
            "/crear_grupo": ["/home", "/crear_grupo"]
        }
        pila_rutas = pila.get(self.page.route, ["/"]) # obtenemos la lista de las pantallas para ruta actual o por defecto la de login
        
        self.page.views.clear() # limpiamos todas las vistas que esten cargadas en la aplicacion
        for ruta in pila_rutas: # recorremos una a una las rutas ded diccionario de rutas y cogemos la vista y su controlador correspondiente
            vista_clase, controlador = self.routes[ruta]
            # comprobamos la vista que toca cargar, si no existe de primeras se crea y se añade a la pantalla
            if vista_clase == VistaPrincipal:
                if not self.vista_principal:
                    # creamos la instancia de la pantalla principal pasando el controlador de usuario[0] y el de mapa[1] para que el mapa siempre esté listo cada vez que se cambie de vista, y grupos[2]
                    self.vista_principal = VistaPrincipal(self.page, controlador[0], controlador[1], controlador[2])
                pantalla = self.vista_principal
            else: # creamos una instancia nueva para el resto de rutas
                pantalla = vista_clase(self.page, controlador)
                # para login y registro enlazamos la pantalla con el controller de auth
                if vista_clase == VistaLogin or vista_clase == VistaRegistro:
                    self.controlador_auth.vista = pantalla
                # para ajustes enlazamos la pantalla con el controller de ajustes
                if vista_clase == VistaAjustes: 
                    self.controlador_ajustes.vista = pantalla
            # creamos la vista física y la añadimos a la pila de navegación para mostrarla
            self.page.views.append(ft.View(route=ruta, controls=[pantalla.vista()], padding=0))

        # sincronizamos los datos y los cargamos
        if vista_clase == VistaPrincipal:
            await self.controlador_usuario.service.sincronizar() # sincronizamos si se ha cambiado algo en otro dispositivo
            if not self.controlador_mapa.geo: # la primera vez que se abre
                self.page.run_task(self.controlador_mapa.iniciar_gps)

        elif vista_clase == VistaAjustes:
            await self.controlador_usuario.service.sincronizar()
            await self.controlador_ajustes.cargar_ajustes()
        self.page.update()