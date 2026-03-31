import flet as ft
import flet_map as ftm

marker_layer_user = ftm.MarkerLayer(markers=[])

def actualizar_marcador_usuario(lat, lon):
    marker_layer_user.markers=[
            ftm.Marker(
                content=ft.Icon(ft.Icons.LOCATION_PIN),
                coordinates=ftm.MapLatitudeLongitude(lat, lon)
            )
        ]
    marker_layer_user.update()

def map(page: ft.Page):
    mapa = ftm.Map( # creacion del mapa
        expand=True, # para que ocupe toda la pantalla
        initial_center=ftm.MapLatitudeLongitude(40.41,-3.70), # el lugar donde comienza al abrir el mapa
        initial_zoom=12, # el zoom inicial
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
            marker_layer_user
        ]
    )

    page.add(mapa)