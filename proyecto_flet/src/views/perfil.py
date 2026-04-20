import flet as ft
import asyncio
from components.componentes import BotonPrincipal, InputTexto
class VistaPerfil:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.controlador.vista = self

        # botón para los ajustes
        self.btn_ajustes = ft.IconButton(
            visible=True, 
            icon=ft.Icons.SETTINGS,
            icon_color="#1A6AFE",
            on_click=self.controlador.ajustes
        )
        # cabecera del perfil con nombre y correo del usuario
        self.usuario = ft.Text(size=20, weight="bold")
        self.email = ft.Text(size=14, color="grey")
        
        self.nombre_input = InputTexto(
            label="Nombre Completo", 
            read_only=True, # EN EL USER CONTROLLER TMB ESTA ESTO, SOBRA EN ALGUNA DE LAS DOS?
            expand=True
        )

        self.apellidos_input = InputTexto(
            label="Apellidos", 
            expand=True
        )

        self.telefono_input = InputTexto(
            label="Teléfono"
        )

        self.pais_input = InputTexto(
            label="País", 
            expand=True
        )

        self.localidad_input = InputTexto(
            label="Localidad", 
            expand=True
        )

        self.mensaje_error = ft.Text(value="", color="red", weight="bold")
        
        self.btn_guardar = BotonPrincipal(
            texto="Guardar cambios",
            icono=ft.Icons.SAVE_AS,
            accion=self.controlador.guardar_cambios
        )

    def vista(self):
        # cargamos los datos del usuario que está iniciado
        asyncio.create_task(self.controlador.cargar_perfil()) # SE LLAMA A LO MISMO QUE EN EL ROUTER, SE PODRIA QUITAR DE AQUI?

        return ft.Container(
            padding=20,
            expand=True, # para ajustar a cualquier dispositivo
            content=ft.Column([
                ft.Row([
                    ft.Text("MI PERFIL", size=25, weight="bold"),
                    self.btn_ajustes
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
                ft.Divider(height=10, color="transparent"), # linea divisoria transparente para que no se muestre
                ft.Row([
                    ft.Column([
                        # dejo pendiente un hueco para el avatar (PDTE. DE VER COMO CONFIGURAR QUE SE PUEDA CAMBIAR)
                        ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.PERSON_OUTLINE),
                            radius=40,
                        ),
                        self.usuario,
                        self.email,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,) 
                ], alignment=ft.MainAxisAlignment.CENTER),

                ft.Divider(height=40, color="black"), # linea divisoria

                # diseño de los campos de la información (formulario)
                ft.Text("Datos Personales", size=16, weight="bold"),
                # fila nombre y apellidos
                ft.Row([
                    self.nombre_input,
                    self.apellidos_input,
                ],spacing=10),

                # fila telefonos
                self.telefono_input,
             
                # fila pais y localidad
                ft.Row([
                    self.pais_input,
                    self.localidad_input,
                ], spacing=10),

                ft.Container(height=10),
                ft.Row([
                    ft.Column([
                        self.btn_guardar,
                        self.mensaje_error
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], scroll=ft.ScrollMode.AUTO, 
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH) # para ensanchar los campos de texto
        )