import flet as ft

class VistaRegistro:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador

        self.nombre_input = ft.TextField(
            label="Nombre Completo",
            hint_text="Introduce tu nombre",
            prefix_icon="person",
            width=300,
            border_radius=10
        )
        
        self.telefono_input = ft.TextField(
            label="Teléfono",
            hint_text="Introduce tu teléfono",
            prefix_icon="phone",
            width=300,
            border_radius=10
        )

        self.email_input = ft.TextField(
            label="Correo Electrónico",
            hint_text="Introduce tu email",
            prefix_icon="mail",
            width=300,
            border_radius=10
        )
        
        self.psw_input = ft.TextField(
            label="Contraseña",
            hint_text="Mínimo 8 caracteres",
            password=True,
            can_reveal_password=True,
            prefix_icon="lock",
            width=300,
            border_radius=10
        )
        
        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

        self.btn_registrar = ft.Button(
            content=ft.Text("Registrarse"),
            icon="app_registration",
            width=200,
            on_click=self.registrar
        )

    async def registrar(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_registrar.disabled = True
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
                    ft.Text("REGISTRO", size=30, weight="bold"),
                    self.nombre_input,
                    self.telefono_input,
                    self.email_input,
                    self.psw_input,
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