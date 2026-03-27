import flet as ft

class VistaPerfil:
    def __init__(self, page: ft.Page, controlador):
        self.page = page
        self.controlador = controlador

# AQUI LA CONFIGURACIÓN DE LA VISTA DEL PERFIL DE USUARIO
# DATOS (nombre, apellidos, pais, localidad, telefono)
# AJUSTES DE CUENTA (datos de acceso (email y pass), cambio de pass, compartir ubicación, eliminar cuenta, cerrar sesión)