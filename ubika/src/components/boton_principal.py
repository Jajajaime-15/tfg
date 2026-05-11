import flet as ft# type: ignore

# para botones como login, registrarse o cualquier funcionalidad principal requerida
class BotonPrincipal(ft.ElevatedButton):
    def __init__(self, texto, icono, accion,ancho=200, color_fondo="#1A6AFE", color_texto="white"):
        super().__init__()
        self.content = ft.Text(texto)
        self.icon = icono
        self.on_click = accion
        self.bgcolor = color_fondo
        self.color = color_texto
        self.width = ancho
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))