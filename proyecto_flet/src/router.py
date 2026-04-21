import flet as ft# type: ignore
from views.login import VistaLogin
from views.registro import VistaRegistro
from views.perfil import VistaPerfil
from views.pricipal import VistaPrincipal
from views.ajustes import VistaAjustes
# Aquí importamos las nuevas vistas que se creen 

class Router:
    def __init__(self, page, controlador_auth, controlador_settings, controlador_user):
        self.page = page
        self.controlador_auth = controlador_auth
        self.controlador_settings = controlador_settings
        self.controlador_user = controlador_user
        # se añadel los controladores de grupos y mapa
        
        # Diccionario de rutas
        self.routes = {
            "/": VistaLogin, # vista iniciar sesión (Alba)
            "/registro": VistaRegistro, # vista registrarse (Alba)
            "/perfil": VistaPerfil, # vista perfil (Alba)
            "/settings": VistaAjustes, # vista ajustes (Alba)
            "/home": VistaPrincipal, # vista principal después de hacer login con grupos (Julio)
        }

    async def route_change(self, e):
        print(f"Cambiando a la ruta: {self.page.route}")
        
        # Limpiamos los controles actuales de la página
        self.page.controls.clear()
        
        # Buscamos la vista en nuestro diccionario y si la ruta no existe, por defecto cargamos el login
        vista_clase = self.routes.get(self.page.route, VistaLogin)
        
        if vista_clase == VistaPrincipal:
            pantalla = VistaPrincipal(self.page, self.controlador_user) # aqui hay que usar el controlador de grupos cuando lo unamos
        elif vista_clase == VistaAjustes:
            pantalla = VistaAjustes(self.page, self.controlador_settings)
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

        self.page.add(pantalla.vista())
        
        # estando en perfil cargamos los datos
        if vista_clase == VistaPerfil:
            await self.controlador_user.cargar_perfil()

        self.page.update()