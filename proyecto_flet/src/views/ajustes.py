import flet as ft
from components.card_password import CardPassword

class VistaAjustes:
    def __init__(self,page,controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self

        # instanciamos la tarjeta para el cambio de contraseña
        self.tarjeta = CardPassword(self.controlador)
    
    def vista(self):
        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW,
                        on_click=lambda _: self.page.go("/")
                    ),
                    ft.Text("Ajustes",size=25, weight="bold")
                ]),
                ft.Divider(height=20),

                ft.Text("Apariencia", size=16, weight="bold", color="#1A6AFE"),
                ft.ListTile( # uso listtile para no tener que estar ajustando filas y columnas 
                    leading=ft.Icon(ft.Icons.PALETTE_OUTLINED),
                    title=ft.Text("Tema de la aplicación"),
                    subtitle=ft.Text("Cambiar entre modo claro y oscuro"),
                    trailing=ft.IconButton(
                        icon=ft.Icons.DARK_MODE,
                        on_click=self.controlador.tema
                    ),
                ),

                ft.Text("Seguridad", size=16, weight="bold", color="#1A6AFE"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOCK_OUTLINED),
                    title=ft.Text("Cambiar contraseña"),
                    subtitle=ft.Text("Actualiza tu clave de acceso"),
                    on_click=lambda _: self.mostrar_cambio_psw(), # llamamos a la funcion que muestra la tarjeta
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=15),
                ),

                # insertamos nuestro componente tarjeta
                self.tarjeta,

                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON_REMOVE_OUTLINED, color="red"),
                    title=ft.Text("Eliminar cuenta", color="red"),
                    subtitle=ft.Text("Borrar todos tus datos permanentemente"),
                    on_click=self.controlador.dialogo,
                ),

                ft.Divider(height=20),

                ft.Text("Cuenta", size=16, weight="bold", color="#1A6AFE"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOGOUT_ROUNDED),
                    title=ft.Text("Cerrar sesión"),
                    on_click=self.controlador.cerrar_sesion,
                ),

            ], scroll=ft.ScrollMode.AUTO)
        )

    # funcion que muetra la tarjeta
    def mostrar_cambio_psw(self):
        self.tarjeta.visible = True
        self.tarjeta.update()