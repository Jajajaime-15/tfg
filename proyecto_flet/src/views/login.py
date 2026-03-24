import flet as ft

class VistaLogin:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador

        self.email_input = ft.TextField(
            label="Correo Electrónico",
            hint_text="Introduce tu email",
            prefix_icon="mail",
            width=300,
            border_radius=10
        )
        
        self.psw_input = ft.TextField(
            label="Contraseña",
            hint_text="Introduce tu contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon="lock",
            width=300,
            border_radius=10
        )
        
        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

        self.btn_entrar = ft.Button(
            content=ft.Text("Iniciar Sesión"),
            icon="login",
            width=200,
            on_click=self.entrar
        )

        self.btn_registro = ft.TextButton(
            content=ft.Text("¿No tienes cuenta? Haz click aquí para registrarte"),
            on_click=self.registrarse
        )

    async def registrarse(self,e):
            await self.page.push_route("/registro")

    # funcion para conectar el boton con el auth_controller
    async def entrar(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_entrar.disabled = True
        self.page.update()

        # llamamos a la función para iniciar sesión(conectarse)
        await self.controlador.conectarse(
            self.email_input, 
            self.psw_input, 
            self.mensaje_error
        )

        # activamos de nuevo el botón
        self.btn_entrar.disabled = False
        self.page.update()

    # función para crear la vista que se mostrará en la pantalla
    def vista(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("LOGIN", size=30, weight="bold"),
                    self.email_input,
                    self.psw_input,
                    self.btn_entrar,
                    self.btn_registro,
                    self.mensaje_error,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            expand=True,
            alignment=ft.Alignment(0, 0),
        )
