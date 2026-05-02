import flet as ft

class VistaLogin:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador

        self.logo = ft.Image(
             src="logo2.png",
             width=200,
             height=120,
             fit="contain"
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
            hint_text="Introduce tu contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.CupertinoIcons.LOCK,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )
        
        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

        self.btn_entrar = ft.ElevatedButton(
            content=ft.Text("Iniciar Sesión"),
            icon=ft.Icons.LOGIN_ROUNDED,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.entrar
        )

        self.btn_recuperar = ft.TextButton(
            content=ft.Text("¿Olvidaste la contraseña? Haz click aquí para recuperarla",
                color="black",
                italic=True
            ),
            on_click=self.recuperar
        )

        self.btn_registro = ft.TextButton(
            content=ft.Text("¿No tienes cuenta? Haz click aquí para registrarte",
                color="black",
                italic=True
            ),
            on_click=self.registrarse
        )

    async def recuperar(self,e):
        await self.controlador.recuperar_psw(self.email_input,self.mensaje_error)

    async def registrarse(self,e):
        self.page.go("/registro")

    # funcion para conectar el boton con el auth_controller
    async def entrar(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_entrar.disabled = True
        self.mensaje_error.value = ""
        self.page.update()

        # llamamos a la función para iniciar sesión(conectarse)
        iniciado =await self.controlador.conectarse(
            self.email_input, 
            self.psw_input, 
            self.mensaje_error
        )

        if iniciado:
            # activamos de nuevo el botón
            self.btn_entrar.disabled = False
            self.page.go("/grupos")
            self.page.update()
        else:
            self.btn_entrar.disabled = False
            self.page.update()    

    # función para crear la vista que se mostrará en la pantalla
    def vista(self):
        return ft.Container(
            content=ft.Column(
                [
                    self.logo,
                    ft.Text("Bienvenido", size=20, weight="bold"),
                    self.email_input,
                    self.psw_input,
                    self.btn_entrar,
                    self.btn_registro,
                    self.btn_recuperar,
                    self.mensaje_error,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            expand=True,
            alignment=ft.Alignment(0, 0),
        )
