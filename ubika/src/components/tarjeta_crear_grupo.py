# components/tarjeta_crear_grupo.py
import flet as ft

def tarjeta_crear_grupo():
    return ft.Column(
        controls=[
            ft.TextField(
                label="Nombre del grupo",
                hint_text="Introduce el nombre del grupo",
                prefix_icon=ft.CupertinoIcons.PERSON,
                focused_border_color="#1A6AFE",
                width=300,
                border_radius=10
            ),
            ft.TextField(
                label="Integrante",
                hint_text="Introduce el nombre del integrante",
                prefix_icon=ft.CupertinoIcons.PERSON,
                focused_border_color="#1A6AFE",
                width=300,
                border_radius=10
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )