import flet as ft # type: ignore
from components.card_password import CardPassword
from components.titulos import TituloSeccion
from components.boton_link import BotonLink

class VistaAjustes:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self
        self.tarjeta_psw = CardPassword(self.controlador)

        self.btn_volver = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW,
            on_click=lambda _: self.page.go("/home")
        )
        self.titulo = ft.Text("Ajustes", size=25, weight="bold")

        self.btn_tema = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            on_click=self.controlador.tema,
            tooltip="Cambiar tema"
        )

        self.btn_mostrar_psw = BotonLink(
            texto="Cambiar mi contraseña",
            accion=self.controlador.mostrar_tarjeta_psw
        )

        self.btn_cerrar_sesion = BotonLink(
            texto="Cerrar sesión activa",
            accion=self.controlador.cerrar_sesion
        )

        self.btn_eliminar_cuenta = ft.TextButton(
            content=ft.Text("Eliminar mi cuenta permanentemente", color="red"),
            on_click=self.controlador.dialogo
        )

        # activar/desactivar ubicacion (por defecto aparece desactivada)
        self.ubicacion = ft.Switch(
            value=False,
            active_color="#1A6AFE",
            on_change = self.controlador.compartir_ubicacion
        )

    def vista(self):
        return ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Divider(height=10),
                    ft.Row([self.btn_volver, self.titulo]),
                    ft.Divider(height=10),

                    TituloSeccion("Apariencia"),
                    ft.Row([
                        ft.Icon(ft.Icons.PALETTE_OUTLINED, color="#1A6AFE"),
                        ft.Text("Tema de la aplicación", size=16),
                        ft.Container(expand=True),
                        self.btn_tema
                    ]),
                    
                    ft.Divider(height=20, color="transparent"),

                    TituloSeccion("Privacidad"),
                    ft.Row([
                        ft.Icon(ft.Icons.EDIT_LOCATION_ALT_OUTLINED, color="#1A6AFE"),
                        ft.Text("Compartir ubicación", size=16),
                        ft.Container(expand=True),
                        self.ubicacion
                    ]),
                    
                    ft.Divider(height=20, color="transparent"),

                    TituloSeccion("Seguridad"),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCK_OUTLINED, color="#1A6AFE"),
                        self.btn_mostrar_psw
                    ]),

                    self.tarjeta_psw, # mostrar/ocultar según el controlador

                    ft.Divider(height=20, color="transparent"),

                    TituloSeccion("Cuenta"),
                    ft.Row([
                        ft.Icon(ft.Icons.LOGOUT_ROUNDED, color="#1A6AFE"),
                        self.btn_cerrar_sesion
                    ]),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON_REMOVE_OUTLINED, color="red"),
                        self.btn_eliminar_cuenta
                    ]),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=10
            ),
            expand=True,
            alignment=ft.Alignment(0, -1), # para que se quede alineado en la parte de arriba
        )