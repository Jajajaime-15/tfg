import flet as ft
from utils.formatear_timestamp import formatear_timestamp

class MapaController:
    def __init__(self, page, gps_service, vista = None):
        self.page = page
        self.service = gps_service
        self.vista = vista
        self.lat = None
        self.lon = None 
        self.geo = None

    async def iniciar_gps(self):
        # llamamos al geolocator
        self.lat, self.lon, self.geo = await self.service.gps(
            actualizar_marcador_usuario = self.actualizar_marcador_usuario, 
            actualizar_marcador_miembros = self.actualizar_marcador_miembros
        ) # le pasamos la pagina y las funciones para dibujar los marcadores

    # funcion para enviar el marcador y la posicion del usuario con cada cambio de posicion
    def actualizar_marcador_usuario(self, datos_usuario, lat, lon, timestamp):
        color_marcador = datos_usuario["color"] # extraemos el color y el nombre propios para poder usarlos
        nombre_marcador = datos_usuario["nombre"]
        inicial = nombre_marcador[0].upper() 

        timestamp_formateado = formatear_timestamp(timestamp)

        marcador = ft.Container( # envolvemos el avatar en un contenedor para pintar un borde y que destaque más en el mapa
            content=ft.CircleAvatar( # creamos el marcador como un avatar circular
                content=ft.Text(inicial, size=14, weight="bold", color="white"),
                bgcolor=color_marcador,
                radius=15
            ),
            border=ft.border.all(2, ft.Colors.BLACK),
            border_radius=50,
            on_click=lambda e: self.vista.mostrar_info_marcador(nombre_marcador, lat, lon, timestamp_formateado) # el evento que permite abrir la info del usuario al pulsar el marcador
        )

        # con el marcador construido y la posicion obtenida llamamos a la vista para pintar el marcador del usuario
        self.vista.pintar_marcador_usuario(marcador, lat, lon) 

    # funcion para enviar el marcador y la posicion del resto de miembros con cada cambio de posicion
    def actualizar_marcador_miembros(self, miembro, datos_miembro, lat, lon, timestamp):
        color_marcador = datos_miembro["color"]
        nombre_marcador = datos_miembro["nombre"]
        inicial = nombre_marcador[0].upper()

        timestamp_formateado = formatear_timestamp(timestamp)

        marcador = ft.Container(
            content=ft.CircleAvatar( # creamos el marcador como un avatar circular
                content=ft.Text(inicial, size=14, weight="bold", color="white"),
                bgcolor=color_marcador,
                radius=15
            ),
            border=ft.border.all(2, ft.Colors.BLACK),
            border_radius=50,
            on_click=lambda e: self.vista.mostrar_info_marcador(nombre_marcador, lat, lon, timestamp_formateado)
        )

        # con el marcador construido y la posicion obtenida llamamos a la vista para pintar el marcador de cada miembro
        self.vista.pintar_marcador_miembros(miembro, marcador, lat, lon)