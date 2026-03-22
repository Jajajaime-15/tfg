import flet as ft
from flet import Checkbox, FloatingActionButton, Icons, Page, TextField
from components.components import PrimaryButton, SecondaryButton, IconButton


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_100)
    page.title = "Login"
    cabecera = ft.Text(
    "¡Bienvenido!", 
    size=40,
    color=ft.Colors.WHITE,
    weight=ft.FontWeight.BOLD,
)
    nombre = TextField(
        hint_text="Nombre", 
        width=250,
        color = ft.Colors.BLACK, 
        bgcolor=ft.Colors.WHITE,
        prefix_icon=ft.CupertinoIcons.PROFILE_CIRCLED,
        border_radius=20,
        autofocus = True)
    password = TextField(
        hint_text="Password", 
        width=250, 
        password=True,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.WHITE,
        prefix_icon = ft.CupertinoIcons.LOCK,
        can_reveal_password=True,
        border_radius=20,
        )
    boton_login = ft.ElevatedButton(
        "LOGIN", 
        width=150,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            color={
                    ft.ControlState.HOVERED: ft.Colors.BLACK,
                    ft.ControlState.FOCUSED: ft.Colors.BLACK,
                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                },
            bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREY_200,
                    ft.ControlState.FOCUSED: ft.Colors.GREY_200,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                },    
    ))
    page.add(
    ft.Container(
        width=400,
        height=500,
        bgcolor=ft.Colors.BLUE,
        border_radius=ft.BorderRadius.all(20),
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), 
            offset=ft.Offset(3, 3)
        ),
        content=ft.Column(
            controls=[
                ft.Container(
                    expand=1,  
                ),
                ft.Row(controls=[cabecera], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    expand=2,  
                ),
                ft.Row(controls=[nombre], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[password], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    expand=8,  
                ),
                ft.Row(
                            controls=[PrimaryButton("LOGIN", width=200)],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                ft.Row(
                            controls=[SecondaryButton("SIGN UP", width=200)],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                ft.Container(
                    expand=8,  
                ),
            ]
        ),
        
        
    )
)


if __name__ == "__main__":
    ft.run(main)