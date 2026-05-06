import flet as ft # type: ignore
from components.boton_principal import BotonPrincipal
from components.input_texto import InputTexto

class VistaRegistro:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self # indicamos al controlador la vista

        self.btn_volver = ft.IconButton(
            visible=True, 
            icon=ft.Icons.ARROW_BACK_IOS,
            icon_color="#1A6AFE",
            on_click=self.volver
        )

        self.nombre_input = InputTexto(
            label="Nombre Completo",
            hint="Introduce tu nombre",
            icono=ft.Icons.PERSON
        )
        
        self.telefono_input = InputTexto(
            label="Teléfono",
            hint="Introduce tu teléfono",
            icono=ft.Icons.PHONE
        )

        self.email_input = InputTexto(
            label="Correo Electrónico",
            hint="Introduce tu email",
            icono=ft.Icons.MAIL
        )
        
        self.psw_input = InputTexto(
            label="Contraseña",
            hint="Mínimo 8 caracteres",
            icono=ft.Icons.LOCK,
            password=True,
            reveal=True
        )

        self.psw_confirmar = InputTexto(
            label="Repetir contraseña",
            hint="Repite tu contraseña",
            icono=ft.Icons.LOCK_RESET,
            password=True,
            reveal=True
        )
        
        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

        self.btn_registrar = BotonPrincipal(
            texto="Registrarse",
            icono=ft.Icons.APP_REGISTRATION,
            accion=self.controlador.registrar_usuario
        )

    async def volver(self, e):
        await self.page.push_route("/")

    # función para crear la vista que se mostrará en la pantalla
    def vista(self):
        return ft.Container(
            padding=ft.padding.only(top=40, left=20, right=20, bottom=20),
            expand = True,
            content=ft.Column(
                [
                    ft.Row(
                        [self.btn_volver],
                        alignment=ft.MainAxisAlignment.START
                    ),

                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Text("REGISTRO", size=30, weight="bold"),
                                margin=ft.Margin.only(
                                    top=10, # espacio desde arriba
                                    bottom=30 # espacio hacia abajo, hacia los campos
                                ), alignment=ft.Alignment(0, 0)
                            ),
                            self.nombre_input,
                            self.telefono_input,
                            self.email_input,
                            self.psw_input,
                            self.psw_confirmar,
                            ft.Container(height=10),
                            self.btn_registrar,
                            self.mensaje_error,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                ],
                spacing = 0
            )
        )