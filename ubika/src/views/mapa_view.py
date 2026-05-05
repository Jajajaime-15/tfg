import flet as ft
import flet_map as ftm # para el mapa
from utils.nominatim import obtener_direccion_legible

class VistaMapa:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self
        self.marker_layer_user = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores propios en el mapa
        self.marker_layer_miembros = ftm.MarkerLayer(markers=[]) # capa para poder dibujar marcadores de los miembros en el mapa
        self.marcadores_miembros = {} # para poder diferenciar cada marcador de cada miembro del grupo
        self.stack = None # creamos el stack antes para luego poder anyadir el geolocator

    def vista(self):
        self.page.padding = 0 # para evitar bordes blancos a los lados

        if self.stack: # en caso de que ya exista el stack del mapa creado no creamos de nuevo el mapa
            return self.stack

        mapa = ftm.Map( # creacion del mapa
            expand=True, # para que ocupe toda la pantalla
            initial_center=ftm.MapLatitudeLongitude(self.controlador.lat, self.controlador.lon), # el lugar donde comienza al abrir el mapa, que sera la ubicacion inicial del usuario
            initial_zoom=12, 
            min_zoom=3,
            max_zoom=23,
            on_tap=None, # lo que hara en caso de pulsar una vez en el mapa 
            on_secondary_tap=None, # lo mismo pero dos veces
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

        self.stack = ft.Stack(controls=[self.controlador.geo, mapa], expand=True) # construimos un stack para que salga por encima siempre el mapa
        return self.stack

    # para anyadir el geo al stack si no se ha agregado antes por no haberse iniciado a tiempo
    def anyadir_geo(self, geo):
        if self.stack and geo not in self.stack.controls: # comprobamos que haya stack y que aun no haya geo añadido al mismo
            self.stack.controls.insert(0, geo) # de esta forma se inserta por debajo de la capa del mapa
            self.page.update()

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
    
    # funcion para mostrar la informacion de cada usuario al pulsar el marcador
    def mostrar_info_marcador(self, nombre, lat, lon, timestamp):
        def cerrar_marcador(e): # para poder cerrar el marcador
            info_marcador.open = False
            self.page.update()

        ubicacion = obtener_direccion_legible(lat, lon) # para obtener desde la api de nominatim una ubicacion que entiendan los usuarios

        info_marcador = ft.AlertDialog( # la ventana que se abre al pulsar el marcador
            content=ft.Column(
                [
                    ft.Text(
                        f"Ubicación: {ubicacion}",
                        color="#000000"
                    ),
                    ft.Text(
                        f"Día y hora de la ubicación: {timestamp}",
                        color="#000000"
                    )
                ],
                tight=True # para que se ajuste al contenido que se muestra
            ),
            title=ft.Text(
                nombre,
                color="#1A6AFE"
            ),
            actions=[
                ft.TextButton(
                    ft.Text("Cerrar"),
                    style=ft.ButtonStyle(color="#1A6AFE"),
                    on_click=cerrar_marcador # al pulsar el boton de cerrar
                )
            ],
            bgcolor="#FFFFFF",
            open=True # para que se abra la ventana
        )

        self.page.overlay.append(info_marcador)
        self.page.update()