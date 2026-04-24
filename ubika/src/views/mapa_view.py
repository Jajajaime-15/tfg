import flet as ft
import flet_map as ftm # para el mapa

class MapaVista:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self
        self.marker_layer_user = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores propios en el mapa
        self.marker_layer_miembros = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores de los miembros en el mapa
        self.marcadores_miembros = {} # para poder diferenciar cada marcador de cada miembro del grupo

    def vista(self):
        self.page.padding = 0 # para evitar bordes blancos a los lados

        mapa = ftm.Map( # creacion del mapa
            expand=True, # para que ocupe toda la pantalla
            initial_center=ftm.MapLatitudeLongitude(self.controlador.lat, self.controlador.lon), # el lugar donde comienza al abrir el mapa, que sera la ubicacion inicial del usuario
            initial_zoom=12, 
            min_zoom=3,
            max_zoom=23,
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
                self.marker_layer_user,
                self.marker_layer_miembros
            ]
        )

        return ft.Stack(controls=[self.controlador.geo, mapa], expand=True) # construimos un stack para que salga por encima siempre el mapa

    # funcion para dibujar el marcador del usuario con cada cambio de posicion
    def pintar_marcador_usuario(self, marcador, lat, lon):
        self.marker_layer_user.markers=[
            ftm.Marker(
                content=marcador,
                coordinates=ftm.MapLatitudeLongitude(lat, lon) # las coordenadas obtenidas de la posicion del usuario
            )
        ]
        self.page.update()

    # funcion para dibujar el marcador del resto de miembros con cada cambio de posicion
    def pintar_marcador_miembros(self, miembro, marcador, lat, lon):
        self.marcadores_miembros[miembro]=ftm.Marker(
            content=marcador,
            coordinates=ftm.MapLatitudeLongitude(lat, lon) # las coordenadas obtenidas de la posicion de cada miembro
        )
        self.marker_layer_miembros.markers = list(self.marcadores_miembros.values())
        self.page.update()