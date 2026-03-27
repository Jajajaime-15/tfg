import flet as ft

from views.login import VistaLogin
from views.registro import VistaRegistro
from views.groups import VistaGrupos
# Aquí importamos las nuevas vistas que se creen 

class Router:
    def __init__(self, page, controlador_auth):
        self.page = page
        self.controlador_auth = controlador_auth
        
        # Diccionario de rutas
        self.routes = {
            "/": VistaLogin,
            "/registro": VistaRegistro,
            "/grupos": VistaGrupos,
        }

    async def route_change(self, e):
        """Función que se activa cada vez que cambia la URL"""
        print(f"Cambiando a la ruta: {self.page.route}")
        
        # Limpiamos los controles actuales de la página
        self.page.controls.clear()
        
        # Buscamos la vista en nuestro diccionario y la ruta no existe, por defecto cargamos el login
        vista_clase = self.routes.get(self.page.route, VistaLogin)
        
        #Instanciamos la vista pasándole el page y el controlador
        # Todas las vistas deben tener (page, controlador) en el __init__
        pantalla = vista_clase(self.page, self.controlador_auth)
        
        # 4. Agregamos la vista a la página y actualizamos
        self.page.add(pantalla.vista())
        self.page.update()