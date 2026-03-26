import flet as ft

class VistaRegistro:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador

        self.btn_volver = ft.IconButton(
            visible=True, 
            icon=ft.Icons.ARROW_BACK_IOS,
            icon_color="#1A6AFE",
            on_click=self.volver
        )

        self.nombre_input = ft.TextField(
            label="Nombre Completo",
            hint_text="Introduce tu nombre",
            prefix_icon=ft.CupertinoIcons.PERSON,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )
        
        self.telefono_input = ft.TextField(
            label="Teléfono",
            hint_text="Introduce tu teléfono",
            prefix_icon=ft.CupertinoIcons.PHONE,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )

        self.email_input = ft.TextField(
            label="Correo Electrónico",
            hint_text="Introduce tu email",
            prefix_icon=ft.CupertinoIcons.MAIL,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )
        
        self.psw_input = ft.TextField(
            label="Contraseña",
            hint_text="Mínimo 8 caracteres",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.CupertinoIcons.LOCK,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )

        self.psw_confirmar = ft.TextField(
            label="Repetir contraseña",
            hint_text="Repite tu contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK_RESET,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )
        
        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

        self.btn_registrar = ft.Button(
            visible=True,
            content=ft.Text("Registrarse"),
            icon=ft.Icons.APP_REGISTRATION,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.registrar
        )

    async def volver(self,e):
            await self.page.push_route("/")

    async def registrar(self, e):
        # comprobamos que las contraseñas coinciden
        if self.psw_input.value != self.psw_confirmar.value:
            self.mensaje_error.value = "Las contraseñas no coinciden"
            self.page.update()
        else:
            # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
            self.btn_registrar.disabled = True
            self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
            self.page.update()

            # llamamos a la función para registrar a un usuario nuevo(registrar_usuario)
            await self.controlador.registrar_usuario(
                self.nombre_input, 
                self.email_input, 
                self.psw_input, 
                self.telefono_input,
                self.mensaje_error
            )

            # activamos de nuevo el botón
            self.btn_registrar.disabled = False
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
                         content=ft.Text("REGISTRO", size=30, weight="bold"),
                         margin=ft.margin.only(
                              top=20, # espacio desde arriba
                              bottom=40 # espacio hacia abajo, hacia los campos
                         ),
                         alignment=ft.Alignment(0, 0)
                    ),
                    self.nombre_input,
                    self.telefono_input,
                    self.email_input,
                    self.psw_input,
                    self.psw_confirmar,
                    self.btn_registrar,
                    self.mensaje_error,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            expand=True,
            alignment=ft.Alignment(0, 0),
        )