import flet as ft
from flet import Checkbox, FloatingActionButton, Icons, Page, TextField


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Login"
    cabecera = ft.Text("LOGIN", size=40, color=ft.Colors.WHITE)
    nombre = TextField(hint_text="Nombre", width=250,color = ft.Colors.BLACK, bgcolor=ft.Colors.WHITE)
    password = TextField(hint_text="Password", width=250, password=True,bgcolor=ft.Colors.WHITE)
    boton_login = ft.ElevatedButton("LOGIN", width=150, bgcolor=ft.Colors.BLACK)
    page.add(
    ft.Container(
        width=400,
        height=500,
        bgcolor=ft.Colors.BLUE,
        border_radius=ft.BorderRadius.all(20),
        padding=20,
        content=ft.Column(
            controls=[
                ft.Container(
                    expand=1,  # Espaciador superior (2 partes)
                ),
                ft.Row(controls=[cabecera], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    expand=2,  # Espaciador superior (2 partes)
                ),
                ft.Row(controls=[nombre], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[password], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    expand=1,  # Espaciador inferior (8 partes)
                ),
                ft.Row(
                            controls=[boton_login],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                ft.Container(
                    expand=8,  # Espaciador inferior (8 partes)
                ),
            ]
        ),
        
        
    )
)


if __name__ == "__main__":
    ft.run(main)