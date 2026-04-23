


class MapaController:
    def __init__(self, page, gps_service, vista = None):
        self.page = page
        self.service = gps_service
        self.vista = vista

    # funcion para dibujar el marcador del usuario con cada cambio de posicion
    def actualizar_marcador_usuario(datos_usuario, lat, lon):
        pass


    # funcion para dibujar el marcador del resto de miembros con cada cambio de posicion
    def actualizar_marcador_miembros(miembro, datos_miembro, lat, lon):
        pass

    