import flet as ft # type: ignore

# este botón es para cualquier accion que usemos que solo sea con icono (guardar, editar, cancelar...)
class BotonAcciones(ft.IconButton):
    def __init__(self, icon, accion, tooltip="", color_icono="#1A6AFE", size=20, ancho=40,  visible=True, deshabilitado=False):
        super().__init__()
        self.icon = icon
        self.on_click = accion
        self.tooltip = tooltip
        self.icon_color = color_icono
        self.icon_size = size
        self.width = ancho
        self.height = ancho
        self.visible = visible
        self.disabled = deshabilitado
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=0)