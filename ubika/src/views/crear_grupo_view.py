import flet as ft # type: ignore
from components.input_texto import InputTexto
from components.boton_principal import BotonPrincipal
from components.titulos import TituloSeccion

class VistaCrearGrupo:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self

        self.btn_volver = ft.IconButton(
            visible=True, 
            icon=ft.Icons.ARROW_BACK_IOS,
            icon_color="#1A6AFE",
            on_click=self.volver
        )

        self.nombre_grupo_input = InputTexto(
            label="Nombre Del Grupo",
            hint="Introduce el nombre del grupo",
            icono=ft.Icons.PERSON,
        )

        self.nombre_integrante_input = InputTexto(
            label="Email Del Integrante",
            hint="Introduce el email del integrante",
            icono=ft.Icons.EMAIL,
            accion=self.crear_grupo
        )

        self.mensaje_error = ft.Text(value="", color="red", weight="bold", visible=True)

        self.btn_crear_grupo = BotonPrincipal(
            texto="Crear Grupo",
            icono=ft.Icons.APP_REGISTRATION,
            accion=self.crear_grupo
        )

    async def volver(self, e):
        await self.page.push_route("/home")

    async def crear_grupo(self, e):
        self.btn_crear_grupo.disabled = True # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        await self.controlador.crear_grupo( # llamamos a la función para crear un grupo
            self.nombre_grupo_input,
            self.nombre_integrante_input
        )

        self.btn_crear_grupo.disabled = False # activamos de nuevo el botón
        self.page.update()

    def vista(self):
        return ft.Container(
            padding=20,
            expand=True,
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                TituloSeccion(texto="CREAR GRUPO", tamanio=30),
                                self.nombre_grupo_input,
                                self.nombre_integrante_input,
                                self.btn_crear_grupo,
                                self.mensaje_error,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                            tight=True,
                        ),
                        alignment=ft.Alignment(0, 0),
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Divider(height=30, color="transparent"),
                            ft.Row(
                                [self.btn_volver], 
                                alignment=ft.MainAxisAlignment.START
                            ),
                        ],
                        tight=True,
                    ),
                ]
            ),
        )