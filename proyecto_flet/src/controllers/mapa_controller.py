import flet as ft
import flet_map as ftm
from proyecto_flet.src.services.gps_service import gps

class MapaController:
    def __init__(self, page, gps_service, vista = None):
        self.page = page
        self.service = gps_service
        self.vista = vista
        self.lat = None
        self.lon = None 
        self.geo = None

    async def iniciar(self):
        # llamamos al geolocator
        self.lat, self.lon, self.geo = await gps(
            self.page, 
            actualizar_marcador_usuario = self.actualizar_marcador_usuario, 
            actualizar_marcador_miembros = self.actualizar_marcador_miembros
        ) # le pasamos la pagina y las funciones para dibujar los marcadores

    # funcion para enviar el marcador y la posicion del usuario con cada cambio de posicion
    def actualizar_marcador_usuario(self, datos_usuario, lat, lon):
        color_marcador = datos_usuario["color"] # extraemos el color y el nombre propios para poder usarlos
        nombre_marcador = datos_usuario["nombre"]
        inicial = nombre_marcador[0].upper() 

        marcador = ft.CircleAvatar( # creamos el marcador como un avatar circular
            content=ft.Text(inicial, size=14, weight="bold", color="white"),
            bgcolor=color_marcador,
            radius=15
        )

        # con el marcador construido y la posicion obtenida llamamos a la vista para pintar el marcador del usuario
        self.vista.pintar_marcador_usuario(marcador, lat, lon) 

    # funcion para enviar el marcador y la posicion del resto de miembros con cada cambio de posicion
    def actualizar_marcador_miembros(self, miembro, datos_miembro, lat, lon):
        color_marcador = datos_miembro["color"]
        nombre_marcador = datos_miembro["nombre"]
        inicial = nombre_marcador[0].upper()

        marcador = ft.CircleAvatar(
            content=ft.Text(inicial, size=14, weight="bold", color="white"),
            bgcolor=color_marcador,
            radius=15
        )

        # con el marcador construido y la posicion obtenida llamamos a la vista para pintar el marcador de cada miembro
        self.vista.pintar_marcador_miembros(miembro, marcador, lat, lon)