'''import flet as ft

def BotonEditar(on_click=None, width=150, disabled=False, loading=False):
    boton = ft.Button(
        content=ft.Icon(ft.Icons.EDIT),
        disabled=disabled or loading,
        on_click=on_click if not disabled and not loading else None,
    )
    return boton'''

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