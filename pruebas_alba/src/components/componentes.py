import flet as ft

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

# campos de texto
class InputTexto(ft.TextField):
    def __init__(self, label, hint="", icono=None, password=False, reveal=False, read_only=False, expand=False):
        super().__init__()
        self.label = label
        self.hint_text = hint
        self.prefix_icon = icono
        self.password = password
        self.can_reveal_password = reveal
        self.read_only = read_only
        self.expand = expand
        self.width = 300 if not expand else None
        self.border_radius = 10
        self.focused_border_color = "#1A6AFE"

# enlaces re registrarse o recuperar contraseña
class BotonLink(ft.TextButton):
    def __init__(self, texto, accion):
        super().__init__()
        self.content = ft.Text(texto, color="black", italic=True)
        self.on_click = accion

# titulos que se uisa por ejemplo en ajustes
class TituloSeccion(ft.Text):
    def __init__(self, texto, color="#1A6AFE"):
        super().__init__()
        self.value = texto
        self.size = 16
        self.weight = "bold"
        self.color = color