import flet as ft
from flet import TextField

class VistaLogin:
    def __init__(self, page, controlador_auth):
        self.page = page
        self.controlador_auth = controlador_auth
    

    def cambiar_vista_registro(self, e):
        self.page.go("/registro")

    def vista(self):
        cabecera = ft.Text(
            "¡Bienvenido!", 
            size=40,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
        )
        nombre = TextField(
            hint_text="Nombre", 
            width=250,
            color=ft.Colors.BLACK, 
            bgcolor=ft.Colors.WHITE,
            prefix_icon=ft.CupertinoIcons.PROFILE_CIRCLED,
            border_radius=20,
            autofocus=True
        )
        password = TextField(
            hint_text="Password", 
            width=250, 
            password=True,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            prefix_icon=ft.CupertinoIcons.LOCK,
            can_reveal_password=True,
            border_radius=20,
        )
        
        return ft.Container(
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
                    ft.Container(expand=1),
                    ft.Row(controls=[cabecera], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(expand=2),
                    ft.Row(controls=[nombre], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[password], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(expand=8),
                    ft.Row(
                        controls=[ft.ElevatedButton("LOGIN", width=200)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[ft.ElevatedButton("SIGN UP", width=200, on_click=self.cambiar_vista_registro)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(expand=8),
                ]
            ),
        )
    
    