import flet as ft
from views.login_view import VistaLogin
from views.registro_view import VistaRegistro
from views.perfil_view import VistaPerfil
from views.principal_view import VistaPrincipal
from views.ajustes_view import VistaAjustes
from views.mapa_view import VistaMapa
# Aquí importamos las nuevas vistas que se creen 

class Router:
    def __init__(self, page, controlador_auth, controlador_settings, controlador_user, controlador_mapa):
        self.page = page
        self.controlador_auth = controlador_auth
        self.controlador_settings = controlador_settings
        self.controlador_user = controlador_user
        self.controlador_mapa = controlador_mapa
        
        # Diccionario de rutas
        self.routes = {
            "/": VistaLogin, # vista iniciar sesión (Alba)
            "/registro": VistaRegistro, # vista registrarse (Alba)
            "/perfil": VistaPerfil, # vista perfil (Alba)
            "/settings": VistaAjustes, # vista ajustes (Alba)
            "/home": VistaPrincipal, # vista principal después de hacer login con grupos (Julio)
            "/mapa": VistaMapa, # vista mapa
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
        elif vista_clase == VistaMapa:
            pantalla = VistaMapa(self.page, self.controlador_mapa)
            self.controlador_mapa.vista = pantalla     
        else: 
            pantalla = VistaLogin(self.page, self.controlador_auth)
            self.controlador_auth.vista = pantalla

        self.page.add(pantalla.vista())
        
        # sincronizamos los datos y los cargamos
        if vista_clase == VistaPrincipal:
            await self.controlador_user.service.sincronizar() # sincronizamos si se ha cambiado algo en otro dispositivo
        elif vista_clase == VistaPerfil:
            self.controlador_user.limpiar_vista() # primero limpiamos la vista de los datos anteriores
            await self.controlador_user.service.sincronizar() # después sincronizamos los datos
            await self.controlador_user.cargar_perfil() # y los cargamos
        elif vista_clase == VistaAjustes:
            await self.controlador_user.service.sincronizar()
            await self.controlador_settings.cargar_ajustes()

        self.page.update()