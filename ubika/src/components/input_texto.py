import flet as ft # type: ignore

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