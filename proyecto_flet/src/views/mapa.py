import flet as ft
import flet_map as ftm
from services.gps_firebase import gps

async def map(page: ft.Page):
    marker_layer_user = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores propios en el mapa
    marker_layer_miembros = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores de los miembros en el mapa
    marcadores_miembros = {}

    # funcion para dibujar el marcador del usuario con cada cambio de posicion
    def actualizar_marcador_usuario(lat, lon):
        marker_layer_user.markers=[
            ftm.Marker(
                content=ft.Icon(ft.Icons.LOCATION_PIN),
                coordinates=ftm.MapLatitudeLongitude(lat, lon) # las coordenadas obtenidas de la posicion del usuario
            )
        ]
        page.update()

    # funcion para dibujar el marcador del resto de miembros con cada cambio de posicion
    def actualizar_marcador_miembros(miembro, lat, lon):
        marcadores_miembros[miembro]=ftm.Marker(
            content=ft.Icon(ft.Icons.LOCATION_ON_ROUNDED),
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