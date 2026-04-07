import flet as ft
import asyncio

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
        
        self.nombre_input = ft.TextField(
            label="Nombre Completo",
            border_radius=10, 
            read_only=True # usamos read_only porque es un campo que no se puede modificar
        )

        self.telefono_input = ft.TextField(
            label="Teléfono",
            border_radius=10
        )

        self.pais_input = ft.TextField(
            label="País",
            border_radius=10,
            expand=True # hacemos que el campo ocupe la mitad de la fila
        )

        self.localidad_input = ft.TextField(
            label="Localidad",
            border_radius=10,
            expand=True # ocupa la otra mitad de la fila de país
        )

        self.mensaje_error = ft.Text(value="", color="red", weight="bold")
        
        self.btn_guardar = ft.ElevatedButton(
            content=ft.Text("Guardar cambios"),
            icon=ft.Icons.SAVE_AS,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.controlador.guardar_cambios
        )

    def vista(self):
        # cargamos los datos del usuario que está iniciado
        asyncio.create_task(self.controlador.cargar_perfil())

        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text("MI PERFIL", size=25, weight="bold"),
                    self.btn_ajustes
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
                ft.Divider(height=10, color="transparent"), # linea divisoria transparente para que no se muestre
                
                ft.Column([
                    # dejo pendiente un hueco para el avatar (PDTE. DE VER COMO CONFIGURAR QUE SE PUEDA CAMBIAR)
                    ft.CircleAvatar(
                        content=ft.Icon(ft.Icons.PERSON_OUTLINE),
                        radius=40,
                    ),
                    self.usuario,
                    self.email,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400 
                ),

                ft.Divider(height=40, color="black"), # linea divisoria

                # diseño de los campos de la información (formulario)
                ft.Text("Datos Personales", size=16, weight="bold"),
                self.nombre_input,
                self.telefono_input,

                # fila para el pais y la localidad
                ft.Row([
                    self.pais_input,
                    self.localidad_input,
                ], spacing=10),

                ft.Container(height=10),

                ft.Column([
                    self.btn_guardar,
                    self.mensaje_error
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400
                )
            ], scroll=ft.ScrollMode.AUTO) # barra para deslizar arriba o abajo
        )