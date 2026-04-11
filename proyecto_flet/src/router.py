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
        """Función que se activa cada vez que cambia la URL"""
        print(f"Cambiando a la ruta: {self.page.route}")
        
        # Limpiamos los controles actuales de la página
        self.page.controls.clear()
        
        # Buscamos la vista en nuestro diccionario y la ruta no existe, por defecto cargamos el login
        vista_clase = self.routes.get(self.page.route, VistaLogin)
        
        if vista_clase == MainLayout:
        #Instanciamos la vista pasándole el page y el controlador
        # Todas las vistas deben tener (page, controlador) en el __init__
            pantalla = MainLayout(self.page, self.controlador_auth.wrapper)
        elif vista_clase == VistaAjustes:
            pantalla = vista_clase(self.page, self.controlador_settings)
        elif vista_clase == VistaPerfil:
            pantalla = VistaPerfil(self.page,self.controlador_user)
            await self.controlador_user.cargar_perfil()
        else:
            pantalla = vista_clase(self.page, self.controlador_auth)
        
        # 4. Agregamos la vista a la página y actualizamos
        self.page.add(pantalla.vista())
        self.page.update()