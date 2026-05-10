import flet as ft 

# campos de texto
class InputTexto(ft.TextField):
    def __init__(self, label, hint="", ancho=300, radio_borde=10, color_borde="#1A6AFE", icono=None, password=False, reveal=False, read_only=False, expand=False, accion=None, visible=True):
        super().__init__()
        self.label = label
        self.hint_text = hint
        self.prefix_icon = icono
        self.password = password
        self.can_reveal_password = reveal
        self.read_only = read_only
        self.expand = expand
        self.width = ancho if not expand else None
        self.border_radius = radio_borde
        self.focused_border_color = color_borde
        self.on_submit = accion
        self.visible = visible