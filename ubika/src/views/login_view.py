import flet as ft # type: ignore
from components.boton_principal import BotonPrincipal
from components.input_texto import InputTexto
from components.boton_link import BotonLink

class VistaLogin:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self

        self.logo = ft.Image(
            src="logo.png",
            width=200,
            height=120,
            fit="contain"
        )

        self.email_input = InputTexto(
            label="Correo Electrónico",
            hint="Introduce tu email",
            icono=ft.Icons.MAIL,
        )
        
        self.psw_input = InputTexto(
            label="Contraseña",
            hint="Introduce tu contraseña",
            password=True,
            reveal=True,
            icono=ft.Icons.LOCK,
        )
        
        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

        self.btn_entrar = BotonPrincipal(
            texto="Iniciar Sesión",
            icono=ft.Icons.LOGIN_ROUNDED,
            accion=self.controlador.conectarse
        )

        self.btn_recuperar = BotonLink(
            texto="¿Olvidaste la contraseña? Haz click aquí para recuperarla",
            accion=self.controlador.recuperar_psw
        )

        self.btn_registro = BotonLink(
            texto="¿No tienes cuenta? Haz click aquí para registrarte",
            accion=self.registro
        )

    async def registro(self, e):
        await self.page.push_route("/registro")

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
