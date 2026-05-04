import flet as ft
from flet import TextField
from components.components import tarjeta_grupos
from components import tarjeta_crear_grupo
from views.perfil_view import VistaPerfil


class VistaGrupos:
    def __init__(self, page, group_controller, user_controller):
        self.page = page
        self.group_controller = group_controller # guardamos el controlador de grupos para usar sus funciones
        self.user_controller = user_controller # guardamos el controlador de user para usar sus funciones
        self.datos_grupo = None
        self.integrantes = None
        self.centro = ft.Container(expand=True)


        self.btn_crear_grupos = ft.ElevatedButton(
            content=ft.Text("Añadir grupo"),
            icon=ft.CupertinoIcons.PLUS,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.crear_grupo
        )


        self.inferior = ft.NavigationBar( # POR QUE ESTA LA BARRA AQUI? NO SE SUPONE QUE LA TENEMOS SOLO EN HOME?
            selected_index=0,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Grupos"),
                ft.NavigationBarDestination(icon=ft.Icons.MAP_OUTLINED, label="Mapa"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINED, label="Perfil"),
            ],
            on_change=self.cambiar_pestana
        )
        

        

        self.mensaje_error = ft.Text(value="", color="red", weight="bold")

    def manejador_tarjeta(self, grupo_nombre):
        async def manejador(e):
            # Seleccionar el grupo para operaciones mas adelante como eliminar o actualizar el nombre
            self.grupo_seleccionado = grupo_nombre
            self.page.update()
        return manejador    

    async def crear_grupo(self, e):
        self.page.go("/crear_grupo")
    
    async def obtener_info_grupos(self):

        # llamamos a la función para crear un grupo
        
        self.datos_grupo, self.integrantes = await self.group_controller.mostrar_grupos(
            self.mensaje_error
        )
        
        # activamos de nuevo el botón
        self.btn_crear_grupos.disabled = False
        self.page.update()    

       

    def eliminar_grupo_desde_tarjeta(self, nombre_grupo):
        print(f"eliminar_grupo_desde_tarjeta llamado con: {nombre_grupo}")  # PRINT DEBUG
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        # llamamos a la función para eliminar un grupo
        self.page.run_task(
        self.group_controller.eliminar_grupo,
        nombre_grupo,
        self.mensaje_error
        )

        # activamos de nuevo el botón
        self.btn_crear_grupos.disabled = False 

    def editar_grupo_desde_tarjeta(self, nombre_actual, nuevo_nombre, callback_ui=None):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        async def realizar_edicion():
            exito = await self.group_controller.editar_grupo(
                nombre_actual, 
                nuevo_nombre, 
                self.mensaje_error
            )
            
            
            if callback_ui:
                callback_ui(exito)
            
            # Actualizar las tarjetas si la edición fue exitosa
            if exito:
                await self.actualizar_tarjetas_grupos()

            # activamos de nuevo el botón
            self.btn_crear_grupos.disabled = False  
            self.page.update()   
            
        self.page.run_task(realizar_edicion)

    def anyadir_integrante_desde_tarjeta(self, nombre_grupo, integrante_field):
        # Funcion para manejar el click en el botón anyadir desde la tarjeta del grupo

        # Extraer el valor del TextField
        nombre_integrante = integrante_field.value
        
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
        self.group_controller.anyadir_participante,
        nombre_grupo,
        nombre_integrante,
        self.mensaje_error
        )

        #AQUI SE ACTUALIZARA LA INFORMACION DE LOS GRUPOS PARA QUE SE VEA EL NUEVO INTEGRANTE

    async def actualizar_tarjetas_grupos(self):
        # obtener info de los grupos
        await self.obtener_info_grupos()

        # Actualizar el contenido del centro con las nueva informacion de los grupos
        self.centro.content = ft.Row(
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    tarjeta_grupos(
                        grupos, 
                        self.integrantes[i] if self.integrantes and i < len(self.integrantes) else [], 
                        on_click_tarjeta=self.manejador_tarjeta(grupos),
                        on_click_anyadir=self.anyadir_integrante_desde_tarjeta  
                    ),
                )
                for i, grupos in enumerate(self.datos_grupo or [])
            ],
        )
        self.page.update()
    

    async def cambiar_pestana(self, e):
        indice = e.control.selected_index # guardamos el indice del botón que se selecciona
        
        if indice == 0:
            await self.actualizar_tarjetas_grupos()
        elif indice == 1:
            # aqui el controlador de mapa y agregamos al centro la vista del mapa
            print ("MAPA JAIME")
        elif indice == 2:
            self.centro.content = VistaPerfil(self.page, self.user_controller).vista() # aqui el controlador de perfil y agregamos al centro la vista del perfil

        self.page.update()     
    
    def vista(self):

        # Construir el contenido inicial del centro (grupos)
        contenido_centro = ft.Row(
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    tarjeta_grupos(grupos, 
                                   self.integrantes[i] if self.integrantes else "", 
                                   on_click_tarjeta=self.manejador_tarjeta(grupos),
                                   on_click_anyadir=self.anyadir_integrante_desde_tarjeta,
                                   on_click_eliminar=self.eliminar_grupo_desde_tarjeta,
                                   on_click_editar=self.editar_grupo_desde_tarjeta,),
                                   
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
                # Centro dinámico (expande para ocupar el espacio)
                ft.Container(expand=True, content=self.centro),
                # Barra de navegación inferior
                self.inferior,
            ],
            spacing=10,
        ),
    )