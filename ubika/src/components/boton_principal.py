import flet as ft # type: ignore

# botones como login, registrarse....
class BotonPrincipal(ft.ElevatedButton):
    def __init__(self, texto, icono, accion):
        super().__init__()
        self.content = ft.Text(texto)
        self.icon = icono
        self.on_click = accion
        self.bgcolor = "#1A6AFE"
        self.color = "white"
        self.width = 200
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))