import flet as ft # type: ignore
from components.tarjeta_psw import TarjetaPsw
from components.titulos import TituloSeccion
from components.boton_link import BotonLink

class VistaAjustes:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self
        self.tarjeta_psw = TarjetaPsw(self.controlador)

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
            accion=self.mostrar_tarjeta_psw
        )

        self.btn_cerrar_sesion = BotonLink(
            texto="Cerrar sesión activa",
            accion=self.controlador.cerrar_sesion
        )

        self.btn_eliminar_cuenta = ft.TextButton(
            content=ft.Text("Eliminar mi cuenta permanentemente", color="red"),
            on_click=self.dialogo
        )

        # activar/desactivar ubicacion (por defecto aparece desactivada)
        self.ubicacion = ft.Switch(
            value=False,
            active_color="#1A6AFE",
            on_change = self.controlador.compartir_ubicacion
        )
        
    # funcion que muetra la tarjeta
    def mostrar_tarjeta_psw(self):
        self.tarjeta_psw.visible = True
        self.page.update()

    # funcion que abre un dialogo de confirmación para eliminar la cuenta
    async def dialogo(self, e):
        self.dialogo_confirmacion = ft.AlertDialog(
            modal=True, # Evita que se cierre haciendo clic fuera
            title=ft.Text("ELIMINAR CUENTA"),
            content=ft.Text("¿Deseas eliminar esta cuenta? Se eliminará toda la información."),
            actions=[
                ft.TextButton("CANCELAR", on_click=lambda _: self.cerrar_dialogo()),
                ft.ElevatedButton(
                    "BORRAR", 
                    on_click=self.controlador.borrar_cuenta, 
                    bgcolor="red", 
                    color="white"
                )
            ]
        )

        self.page.overlay.append(self.dialogo_confirmacion)
        # abrimos el dialogo
        self.dialogo_confirmacion.open=True
        self.page.update()

    # funcion que cierra el AlertDialog
    def cerrar_dialogo(self):
        for control in self.page.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        self.page.update()

    def vista(self):
        return ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Divider(height=30, color="transparent"),
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