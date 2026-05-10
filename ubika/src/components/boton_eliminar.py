import flet as ft

class BotonEliminar(ft.ElevatedButton):
    def __init__(self, accion, ancho=150, color_fondo="red", color_texto="white", deshabilitado=False):
        super().__init__()
        self.content = ft.Icon(ft.Icons.DELETE)
        self.on_click = accion
        self.bgcolor = color_fondo
        self.color = color_texto
        self.disabled = deshabilitado
        self.width = ancho
        self.height = ancho
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=0)