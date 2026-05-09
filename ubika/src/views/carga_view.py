import flet as ft # type: ignore

class VistaCarga:
    def __init__(self, page):
        self.page = page

        self.logo = ft.Image(
            src="logo.png",
            width=150,
            height=150,
            fit="contain"
        )

        # indicador de carga circular con un texto debajo
        self.loader = ft.ProgressRing(
            width=40, 
            height=40, 
            stroke_width=4, 
            color="#1A6AFE"
        )

        self.texto_estado = ft.Text(
            "Cargando configuración...",
            size=14,
            italic=True,
            color=ft.Colors.GREY_500
        )

    def vista(self):
        return ft.Container(
            content=ft.Column(
                [
                    self.logo,
                    ft.Divider(height=20, color="transparent"),
                    self.loader,
                    ft.Divider(height=10, color="transparent"),
                    self.texto_estado,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=ft.Colors.BLACK if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.WHITE
        )