import flet as ft # type: ignore
from components.input_texto import InputTexto
from components.boton_principal import BotonPrincipal

class CardPassword(ft.Card):
    def __init__(self,controlador):
        super().__init__()
        self.controlador = controlador
        self.visible = False # esta tarjeta/componente no aparece hasta que no se ejecuta la funcion de cambiar contraseña

        self.psw_nueva = InputTexto(
            label = "Nueva contraseña",
            password = True,
            reveal = True
        )
        self.psw_confirmar = InputTexto(
            label = "Confirmar contraseña",
            password = True,
            reveal = True,
            accion = self.guardar
        )
        self.mensaje_error = ft.Text(value="",color="red",weight="bold")

        self.content=ft.Container(
            padding=20,
            bgcolor="surfacevariant",
            border_radius=15,
            content=ft.Column([
                ft.Text("Cambiar Contraseña", size=18, weight="bold"),
                self.psw_nueva,
                self.psw_confirmar,
                self.mensaje_error,
                ft.Row([
                    ft.TextButton("CANCELAR", on_click=self.cerrar),
                    BotonPrincipal(
                        texto="ACTUALIZAR",
                        ancho=None,
                        icono=None,
                        accion=self.guardar,
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=15, tight=True)
        )

    # funcion que cierra el componente
    def cerrar(self, e):
        self.visible = False
        # dejamos los campos limpios para que cuando se vuelva a abrir estén vacios
        # RECUERDO QUE EN UN CONTROLLER TMB HACES LIMPIEZA, AUNQUE SEA EN ACCIONES DIFERENTES QUIZAS RENTA UNA FUNCION SEPARADA QUE SE LLAME LIMPIAR Y SE USE EN VARIOS APARTADOS
        # ESTO PODRIA IR EN UNA CARPETA NUEVA LLAMADA UTILS, PERO CLARO ESTO SERIA UN CASO QUIZAS DEMASIADO CONCRETO, VALORALO
        self.psw_nueva.value = "" 
        self.psw_confirmar.value = ""
        self.mensaje_error.value = ""
        self.update()

    # funcion que hace de puente para guardar
    async def guardar(self, e):
        await self.controlador.cambio_psw(self)