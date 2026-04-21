import flet as ft # type: ignore

# titulos que se uisa por ejemplo en ajustes
class TituloSeccion(ft.Text):
    def __init__(self, texto, color="#1A6AFE"):
        super().__init__()
        self.value = texto
        self.size = 16
        self.weight = "bold"
        self.color = color