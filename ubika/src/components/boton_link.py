import flet as ft

# para los enlaces de registrarse o recuperar contraseña
class BotonLink(ft.TextButton):
    def __init__(self, texto, accion):
        super().__init__()
        self.content = ft.Text(texto, color=ft.Colors.ON_SURFACE)
        self.on_click = accion