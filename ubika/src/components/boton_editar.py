import flet as ft

class BotonEditar(ft.ElevatedButton):
    def __init__(self, accion, color_fondo="#1A6AFE", color_texto="white", ancho=150, deshabilitado=False):
        super().__init__()
        self.content = ft.Icon(ft.Icons.EDIT)
        self.on_click = accion
        self.bgcolor = color_fondo
        self.color = color_texto
        self.width = ancho
        self.height = ancho
        self.disabled = deshabilitado
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=0)