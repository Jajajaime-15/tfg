import flet as ft

from views.login_view import VistaLogin
from views.registro import VistaRegistro
from views.groups_view import VistaGrupos
from controllers.auth_controller import AuthController
from controllers.group_controller import GroupController
from controllers.user_controller import UserController
# Aquí importamos las nuevas vistas que se creen 

class Router:
    def __init__(self, page, wrapper):
        self.page = page
        self.wrapper = wrapper
        self.auth_controller = AuthController(page, wrapper)
        self.group_controller = GroupController(page, wrapper)
        self.user_controller = UserController(page, wrapper)  
          
        
        # Diccionario de rutas
        self.routes = {
            "/": (VistaLogin, self.auth_controller),
            "/registro": (VistaRegistro, self.auth_controller),
            "/grupos": (VistaGrupos, self.group_controller, self.user_controller), # pasamos ambos controladores a la vista de grupos para poder usar las funciones de ambos
        }

    async def route_change(self, e):
        """Función que se activa cada vez que cambia la URL"""
        print(f"Cambiando a la ruta: {self.page.route}")
        
        # Limpiamos los controles actuales de la página
        self.page.controls.clear()
        
        if self.page.route == "/":
            pantalla = VistaLogin(self.page, self.auth_controller)
            
        elif self.page.route == "/registro":
            pantalla = VistaRegistro(self.page, self.auth_controller)
            
        elif self.page.route == "/grupos":
            #Pasamos dos controladores a VistaGrupos
            pantalla = VistaGrupos(self.page, self.group_controller, self.user_controller)
            await pantalla.obtener_info_grupos()  # Cargar datos iniciales
        else:
            # Ruta no encontrada, redirigir a login
            pantalla = VistaLogin(self.page, self.auth_controller)
        
        # Agregamos la vista a la página
        self.page.add(pantalla.vista())
        self.page.update()