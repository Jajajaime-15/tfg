import flet as ft

class VistaCrearGrupo:
    def __init__(self, page,controlador):
        self.page = page
        self.controlador = controlador

        self.btn_volver = ft.IconButton(
            visible=True, 
            icon=ft.Icons.ARROW_BACK_IOS,
            icon_color="#1A6AFE",
            on_click=self.volver
        )

        self.nombre_grupo_input = ft.TextField(
            label="Nombre Del Grupo",
            hint_text="Introduce el nombre del grupo",
            prefix_icon=ft.CupertinoIcons.PERSON,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )

        self.nombre_integrante_input = ft.TextField(
            label="Nombre Del Integrante",
            hint_text="Introduce el email del integrante",
            prefix_icon=ft.CupertinoIcons.PERSON,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )
        
        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

        self.btn_crear_grupo = ft.ElevatedButton(
            content=ft.Text("Crear Grupo"),
            icon=ft.Icons.APP_REGISTRATION,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.crear_grupo
        )

    async def volver(self,e):
        self.page.go("/grupos")

    async def crear_grupo(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupo.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        # llamamos a la función para crear un grupo
        await self.controlador.crear_grupo(
            self.nombre_grupo_input,
            self.nombre_integrante_input,
            self.mensaje_error
        )

        # activamos de nuevo el botón
        self.btn_crear_grupo.disabled = False
        self.page.update()

    # función para crear la vista que se mostrará en la pantalla
    def vista(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                         [self.btn_volver],
                         alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Container(
                         content=ft.Text("CREAR GRUPO", size=30, weight="bold"),
                         margin=ft.margin.only(
                              top=20, # espacio desde arriba
                              bottom=40 # espacio hacia abajo, hacia los campos
                         ),
                         alignment=ft.Alignment(0, 0)
                    ),
                    self.nombre_grupo_input,
                    self.nombre_integrante_input,
                    self.btn_crear_grupo,
                    self.mensaje_error,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            expand=True,
            alignment=ft.Alignment(0, 0),
        )