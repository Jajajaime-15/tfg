import flet as ft
import flet_map as ftm # para el mapa
from proyecto_flet.src.services.gps_service import gps


class MapaVista:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self

    def vista(self):
        pass

async def map(page: ft.Page):
    page.padding = 0 # para evitar bordes blancos a los lados

    marker_layer_user = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores propios en el mapa
    marker_layer_miembros = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores de los miembros en el mapa
    marcadores_miembros = {} # para poder diferenciar cada marcador de cada miembro del grupo

    # funcion para dibujar el marcador del usuario con cada cambio de posicion
    def actualizar_marcador_usuario(datos_usuario, lat, lon):
        color_marcador = datos_usuario["color"] # extraemos el color y el nombre propios para poder usarlos
        nombre_marcador = datos_usuario["nombre"]
        inicial = nombre_marcador[0].upper() 

        marcador = ft.CircleAvatar( # creamos el marcador como un avatar circular
            content=ft.Text(inicial, size=14, weight="bold", color="white"),
            bgcolor=color_marcador,
            radius=15
        )

        marker_layer_user.markers=[
            ftm.Marker(
                content=marcador,
                coordinates=ftm.MapLatitudeLongitude(lat, lon) # las coordenadas obtenidas de la posicion del usuario
            )
        ]
        page.update()

    # funcion para dibujar el marcador del resto de miembros con cada cambio de posicion
    def actualizar_marcador_miembros(miembro, datos_miembro, lat, lon):
        # realizamos lo mismo que en el usuario pero con el resto de los miembros
        color_marcador = datos_miembro["color"]
        nombre_marcador = datos_miembro["nombre"]
        inicial = nombre_marcador[0].upper()

        marcador = ft.CircleAvatar(
            content=ft.Text(inicial, size=14, weight="bold", color="white"),
            bgcolor=color_marcador,
            radius=15
        )

        marcadores_miembros[miembro]=ftm.Marker(
            content=marcador,
            coordinates=ftm.MapLatitudeLongitude(lat, lon) # las coordenadas obtenidas de la posicion de cada miembro
        )
        marker_layer_miembros.markers = list(marcadores_miembros.values())
        page.update()

    # llamamos al geolocator
    lat, lon, geo = await gps(
        page, 
        actualizar_marcador_usuario= actualizar_marcador_usuario, 
        actualizar_marcador_miembros= actualizar_marcador_miembros
    ) # le pasamos la pagina y las funciones para dibujar los marcadores

    mapa = ftm.Map( # creacion del mapa
        expand=True, # para que ocupe toda la pantalla
        initial_center=ftm.MapLatitudeLongitude(lat, lon), # el lugar donde comienza al abrir el mapa, que sera la ubicacion inicial del usuario
        initial_zoom=12, 
        min_zoom=3,
        max_zoom=25,
        on_tap=None, # lo que hara en caso de pulsar una vez en el mapa 
        on_secondary_tap=None, # lo mismo pero dos veces
        on_event=print, # lo que hara en cada evento del mapa, para depurar he puesto que imprima cada accion en la consola
        interaction_configuration=ftm.InteractionConfiguration( 
            flags=ftm.InteractionFlag.ALL # para habilitar todas las opciones de interaccion con el mapa (zoom, drag, etc)
        ),
        layers=[ # las capas que componen el mapa
            ftm.TileLayer( # esta es la capa basica que va en cualquier mapa la primera
                url_template="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png", # el mapa que usamos, en este caso el de CartoDB
                on_image_error=lambda e: print("TileLayer Error") # en caso de que salte error avisamos por la consola
            ),
            marker_layer_user,
            marker_layer_miembros
        ]
    )

    page.add(ft.Stack(controls=[geo, mapa], expand=True))