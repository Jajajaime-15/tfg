import flet as ft

from views.login import VistaLogin
from views.registro import VistaRegistro
from views.perfil import VistaPerfil
from  views.home_prueba import MainLayout
from views.ajustes import VistaAjustes
# Aquí importamos las nuevas vistas que se creen 

class Router:
    def __init__(self, page, controlador_auth, controlador_settings, controlador_user):
        self.page = page
        self.controlador_auth = controlador_auth
        self.controlador_settings = controlador_settings
        self.controlador_user = controlador_user
        
        # Diccionario de rutas
        self.routes = {
            "/": VistaLogin, # vista iniciar sesión (Alba)
            "/registro": VistaRegistro, # vista registrarse (Alba)
            "/perfil": VistaPerfil, # vista perfil (Alba)
            "/settings": VistaAjustes, # vista ajustes (Alba)
            "/home": MainLayout, # vista principal con grupos (Julio)
        }

    async def route_change(self, e):
        print(f"Cambiando a la ruta: {self.page.route}")
        
        # Limpiamos los controles actuales de la página
        self.page.controls.clear()
        
        # Buscamos la vista en nuestro diccionario y la ruta no existe, por defecto cargamos el login
        vista_clase = self.routes.get(self.page.route, VistaLogin)
        
        if vista_clase == MainLayout:
            pantalla = MainLayout(self.page, self.controlador_auth.wrapper)
        elif vista_clase == VistaAjustes:
            pantalla = vista_clase(self.page, self.controlador_settings)
            self.controlador_settings.vista = pantalla
        elif vista_clase == VistaPerfil:
            pantalla = VistaPerfil(self.page, self.controlador_user)
            self.controlador_user.vista = pantalla   
        elif vista_clase == VistaRegistro:
            pantalla = VistaRegistro(self.page, self.controlador_auth)
            self.controlador_auth.vista = pantalla     
        else: 
            pantalla = VistaLogin(self.page, self.controlador_auth)
            self.controlador_auth.vista = pantalla

        # indicamos al controlador de auth la vista que tiene que usar
        if vista_clase in [VistaLogin, VistaRegistro]:
                self.controlador_auth.vista = pantalla
                
        self.page.add(pantalla.vista())
        
        # estando en perfil cargamos los datos
        if vista_clase == VistaPerfil:
            await self.controlador_user.cargar_perfil()

        self.page.update()