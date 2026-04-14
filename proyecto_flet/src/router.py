import flet as ft

from views.login import VistaLogin
from views.registro import VistaRegistro
from views.groups import VistaGrupos
from controllers.auth_controller import AuthController
from controllers.group_controller import GroupController
# Aquí importamos las nuevas vistas que se creen 

class Router:
    def __init__(self, page, wrapper):
        self.page = page
        self.wrapper = wrapper
        self.auth_controller = AuthController(page, wrapper)
        self.group_controller = GroupController(page, wrapper)
        
        # Diccionario de rutas
        self.routes = {
            "/": (VistaLogin, self.auth_controller),
            "/registro": (VistaRegistro, self.auth_controller),
            "/grupos": (VistaGrupos, self.group_controller), 
        }

    async def route_change(self, e):
        """Función que se activa cada vez que cambia la URL"""
        print(f"Cambiando a la ruta: {self.page.route}")
        
        # Limpiamos los controles actuales de la página
        self.page.controls.clear()
        
        # Buscamos la vista en nuestro diccionario y la ruta no existe, por defecto cargamos el login
        vista_clase, controlador = self.routes.get(self.page.route, (VistaLogin, self.auth_controller))
        
        #Instanciamos la vista pasándole el page y el controlador
        # Todas las vistas deben tener (page, controlador) en el __init__
        pantalla = vista_clase(self.page, controlador)
        
        # 4. Agregamos la vista a la página y actualizamos
        if isinstance(pantalla, VistaGrupos):
            await pantalla.obtener_info_grupos() # llamamos a la función para obtener los datos de los grupos
        self.page.add(pantalla.vista())
        self.page.update()