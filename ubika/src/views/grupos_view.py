import flet as ft
from components.tarjeta_grupos import tarjeta_grupos

class VistaGrupos:
    def __init__(self, page, grupos_controller):
        self.page = page
        self.grupos_controller = grupos_controller # guardamos el controlador de grupos para usar sus funciones
        self.datos_grupo = None
        self.integrantes = None
        self.emails = None
        self.centro = ft.Container(expand=True)

        self.btn_crear_grupos = ft.ElevatedButton(
            content=ft.Text("Añadir grupo"),
            icon=ft.Icons.ADD,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.crear_grupo
        )

        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

    def manejador_tarjeta(self, grupo_nombre):
        async def manejador(e):
            self.grupo_seleccionado = grupo_nombre # Seleccionar el grupo para operaciones mas adelante como eliminar o actualizar el nombre
            self.page.update()
        return manejador    

    async def crear_grupo(self, e):
        self.page.go("/crear_grupo")
    
    async def obtener_info_grupos(self):
        self.datos_grupo, self.integrantes, self.emails = await self.grupos_controller.mostrar_grupos(self.mensaje_error)
        self.btn_crear_grupos.disabled = False # activamos de nuevo el botón
        self.page.update()    

    def eliminar_integrante_desde_tarjeta(self, e, nombre_grupo, email_integrante):
        print(f"Eliminando integrante: {email_integrante} del grupo: {nombre_grupo}")
        
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = ""
        self.page.update()
        
        self.page.run_task(
            self.grupos_controller.eliminar_participante,
            nombre_grupo,
            email_integrante,
            self.mensaje_error
        )
        
        self.btn_crear_grupos.disabled = False
        self.page.update()

    def eliminar_grupo_desde_tarjeta(self, nombre_grupo):
        self.btn_crear_grupos.disabled = True # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        self.page.run_task( # llamamos a la función para eliminar un grupo
            self.grupos_controller.eliminar_grupo,
            nombre_grupo,
            self.mensaje_error
        )

        self.btn_crear_grupos.disabled = False # activamos de nuevo el botón

    def editar_grupo_desde_tarjeta(self, nombre_actual, nuevo_nombre, callback_ui=None):
        if nuevo_nombre is None: # Si nuevo_nombre es None es porque entró en modo edicion
            return
        
        # Resto del código para guardar cambios
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = ""
        self.page.update()

        async def realizar_edicion():
            exito = await self.grupos_controller.editar_grupo(
                nombre_actual, 
                nuevo_nombre, 
                self.mensaje_error
            )
            
            if callback_ui:
                callback_ui(exito)
            
            if exito:
                await self.actualizar_tarjetas_grupos()

            self.btn_crear_grupos.disabled = False  
            self.page.update()   
            
        self.page.run_task(realizar_edicion)

    def anyadir_integrante_desde_tarjeta(self, nombre_grupo, integrante_field):
        # Funcion para manejar el click en el botón anyadir desde la tarjeta del grupo
        nombre_integrante = integrante_field.value # Extraer el valor del TextField
        
        # Validar que no esté vacío
        if not nombre_integrante or nombre_integrante.strip() == "":
            integrante_field.error_text = "El nombre del integrante no puede estar vacío"
            integrante_field.value = ""
            self.page.update()
            return
        
        # Limpiar errores y el valor del TextField para la proxima vez
        integrante_field.error_text = None
        integrante_field.value = ""
        
        self.page.run_task(
            self.grupos_controller.anyadir_participante,
            nombre_grupo,
            nombre_integrante,
            self.mensaje_error
        )

    async def actualizar_tarjetas_grupos(self):
        await self.obtener_info_grupos()

        self.centro.content = ft.Row(
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    tarjeta_grupos(
                        grupos, 
                        self.integrantes[i] if self.integrantes and i < len(self.integrantes) else [], 
                        self.emails[i] if self.emails and i < len(self.emails) else [],
                        on_click_tarjeta=self.manejador_tarjeta(grupos),
                        on_click_anyadir=self.anyadir_integrante_desde_tarjeta,
                        on_click_eliminar=self.eliminar_grupo_desde_tarjeta,
                        on_click_editar=self.editar_grupo_desde_tarjeta,
                        on_click_eliminar_integrante=self.eliminar_integrante_desde_tarjeta,
                    ),
                )
                for i, grupos in enumerate(self.datos_grupo or [])
            ],
        )
        self.page.update()

    def vista(self):
        # Construir el contenido inicial del centro (grupos)
        contenido_centro = ft.Row(
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    tarjeta_grupos(
                        grupos, 
                        self.integrantes[i] if self.integrantes else "", 
                        self.emails[i] if self.emails and i < len(self.emails) else [],
                        on_click_tarjeta=self.manejador_tarjeta(grupos),
                        on_click_anyadir=self.anyadir_integrante_desde_tarjeta,
                        on_click_eliminar=self.eliminar_grupo_desde_tarjeta,
                        on_click_editar=self.editar_grupo_desde_tarjeta,
                        on_click_eliminar_integrante=self.eliminar_integrante_desde_tarjeta,
                    ),
                )
                for i, grupos in enumerate(self.datos_grupo or [])
            ],
        )

        self.centro.content = contenido_centro

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.BorderRadius.all(20),
            padding=20,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), 
                offset=ft.Offset(3, 3)
            ),
            content=ft.Column(
                expand=True,
                controls=[
                    # Fila superior con formulario
                    ft.Container(
                        content=ft.Row([
                            ft.Text("Mis Grupos", size=40, weight="bold", color="BLACK"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,),
                    ),
                    ft.Row(
                        controls=[
                            self.btn_crear_grupos,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    self.mensaje_error,
                    ft.Container(expand=True, content=self.centro), # Centro dinámico (expande para ocupar el espacio)
                ],
                spacing=10,
            ),
        )