import flet as ft
from flet import TextField


class VistaGrupos:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador

        self.nombre_grupo_input = ft.TextField(
            label="Nombre Completo",
            hint_text="Introduce tu nombre",
            prefix_icon=ft.CupertinoIcons.PERSON,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )

        self.btn_crear_grupo = ft.ElevatedButton(
            content=ft.Text("Crear grupo"),
            icon=ft.Icons.APP_REGISTRATION,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.crear_grupo
        )

        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

    async def crear_grupo(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupo.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        # llamamos a la función para registrar a un usuario nuevo(registrar_usuario)
        await self.controlador.crear_grupo(
            self.nombre_grupo_input,
            self.mensaje_error
        )

        # activamos de nuevo el botón
        self.btn_crear_grupo.disabled = False
        self.page.update()    

    def vista(self):
        
    
        
        
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
                    ft.Row(controls=[self.nombre_grupo_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[self.btn_crear_grupo], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(expand=8),
                ]
            ),
        )    