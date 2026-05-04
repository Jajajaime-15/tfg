import flet as ft # type: ignore
import asyncio
from components.boton_principal import BotonPrincipal
from components.input_texto import InputTexto

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

        # avatar
        self.inicial_texto = ft.Text(
            value="", 
            size=30, 
            weight="bold", 
            color="white"
        )

        self.avatar = ft.CircleAvatar(
            content=self.inicial_texto,
            radius=40,
            bgcolor="TRANSPARENT",
        )

        self.contenedor_avatar = ft.Container(
            content=self.avatar,
            alignment=ft.Alignment(0, 0),
            padding=20,
            on_click=self.controlador.mostrar_colores,
        )

        self.lista_colores = ft.BottomSheet(
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("Personalizar avatar",
                            size=20,
                            weight="bold"),
                    ft.Divider(),
                    ft.Row([
                        self.crear_boton_color("Azul", "#1A6AFE"),
                        self.crear_boton_color("Rojo", "red"),
                        self.crear_boton_color("Verde", "green"),
                        self.crear_boton_color("Naranja", "orange"),
                        self.crear_boton_color("Morado", "purple"),
                        self.crear_boton_color("Rosa", "pink"),
                    ], 
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=50), # añadimos una linea invisible para separar de la barra de navegación del movil
                ],
                tight=True),
            )
        )

        # cabecera del perfil con nombre y correo del usuario
        self.usuario = ft.Text(size=20, weight="bold")
        self.email = ft.Text(size=14, color="grey")
        
        self.nombre_input = InputTexto(
            label="Nombre Completo",
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

    # funcion que crea el boton para el color creando un icono para elegirlo
    def crear_boton_color(self,nombre,color_valor):
        return ft.IconButton(
            icon=ft.Icons.CIRCLE,
            icon_color=color_valor,
            icon_size=40,
            tooltip=nombre,
            on_click= self.controlador.seleccionar_color,
            data=color_valor # usamos data para aceptar el color y que se modifique el avatar
        )
    def vista(self):
        
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
                        self.contenedor_avatar,
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