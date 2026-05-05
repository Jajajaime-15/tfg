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
        
        # Diccionario de rutas
        self.routes = {
            "/": VistaLogin, # vista iniciar sesión (Alba)
            "/registro": VistaRegistro, # vista registrarse (Alba)
            "/settings": VistaAjustes, # vista ajustes (Alba)
            "/home": VistaPrincipal # vista principal después de hacer login con grupos (Julio)
        }

    async def cambiar_ruta(self, e):
        print(f"Cambiando a la ruta: {self.page.route}")
        
        # Limpiamos los controles actuales de la página
        self.page.controls.clear()
        
        # Buscamos la vista en nuestro diccionario y si la ruta no existe, por defecto cargamos el login
        vista_clase = self.routes.get(self.page.route, VistaLogin)
        
        if vista_clase == VistaPrincipal: # esta vista carga grupos, perfil y mapa y se manejan desde su vista
            if not self.vista_principal: # la primera vez que se abre
                self.vista_principal = VistaPrincipal(self.page, self.controlador_user, self.controlador_mapa)
            pantalla = self.vista_principal
        elif vista_clase == VistaAjustes:
            pantalla = VistaAjustes(self.page, self.controlador_settings)
            self.controlador_settings.vista = pantalla
        elif vista_clase == VistaRegistro:
            pantalla = VistaRegistro(self.page, self.controlador_auth)
            self.controlador_auth.vista = pantalla
        else: 
            pantalla = VistaLogin(self.page, self.controlador_auth)
            self.controlador_auth.vista = pantalla

        self.page.add(pantalla.vista())
        
        # sincronizamos los datos y los cargamos
        if vista_clase == VistaPrincipal:
            await self.controlador_user.service.sincronizar() # sincronizamos si se ha cambiado algo en otro dispositivo
            if not self.controlador_mapa.geo: # la primera vez que se abre
                self.page.run_task(self.controlador_mapa.iniciar_gps)
        elif vista_clase == VistaAjustes:
            await self.controlador_user.service.sincronizar()
            await self.controlador_settings.cargar_ajustes()

        self.page.update()