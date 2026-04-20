import flet as ft
from flet import TextField
from components.components import tarjeta_grupos
from views.perfil import VistaPerfil
from controllers.user_controller import UserController # NO DEBERIA LLEGAR DESDE ROUTER EN VEZ DE CREARSE AQUI?
from controllers.group_controller import GroupController # llamas al controlador de grupos


class VistaGrupos:
    def __init__(self, page, controlador):
        self.page = page
        self.controlador = controlador
        self.datos_grupo = None
        self.integrantes = None
        self.centro = ft.Container(expand=True)
        

        self.nombre_grupo_input = ft.TextField(
            label="Nombre del grupo",
            hint_text="Introduce el nombre del grupo",
            prefix_icon=ft.CupertinoIcons.PERSON,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )

        self.integrante_input = ft.TextField(
            label="Integrante",
            hint_text="Introduce el nombre del integrante",
            prefix_icon=ft.CupertinoIcons.PERSON,
            focused_border_color="#1A6AFE",
            width=300,
            border_radius=10
        )


        self.btn_crear_grupos = ft.ElevatedButton(
            content=ft.Text("Crear grupo"),
            icon=ft.Icons.APP_REGISTRATION,
            bgcolor="#1A6AFE",
            color="white",
            width=200,
            on_click=self.crear_grupo
        )

        self.btn_eliminar_grupo = ft.ElevatedButton(
            content=ft.Text("Eliminar grupo"),
            icon=ft.Icons.DELETE,
            bgcolor="#FF4136",
            color="white",
            width=200,
            on_click=self.eliminar_grupo
        )
        
        self.btn_anyadir_integrante = ft.ElevatedButton(
            content=ft.Text("Añadir integrante"),
            icon=ft.Icons.DELETE, # DELETE PARA AÑADIR?
            bgcolor="#FF4136",
            color="white",
            width=200,
            on_click=self.anyadir_integrante
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

    async def crear_grupo(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        # llamamos a la función para crear un grupo
        await self.controlador.crear_grupo(
            self.nombre_grupo_input,
            self.integrante_input,
            self.mensaje_error
        )
    
    async def obtener_info_grupos(self):

        # llamamos a la función para crear un grupo
        
        self.datos_grupo, self.integrantes = await self.controlador.mostrar_grupos(
            self.mensaje_error
        )
        
        # obtenemos solo los nombres de los grupos para mostrarlos en las tarjetas
        print(f"Grupos disponibles: {self.datos_grupo}") # mostramos en consola los grupos disponibles para comprobar que se están recuperando correctamente
        

        # activamos de nuevo el botón
        self.btn_crear_grupos.disabled = False
        self.page.update()    

       

    async def eliminar_grupo(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        # llamamos a la función para eliminar un grupo
        await self.controlador.eliminar_grupo(
            self.nombre_grupo_input,
            self.mensaje_error
        )

        # activamos de nuevo el botón
        self.btn_crear_grupos.disabled = False
        self.page.update()        

    async def anyadir_integrante(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        # llamamos a la función para añadir un integrante a un grupo
        await self.controlador.anyadir_participante(
            self.nombre_grupo_input,
            self.integrante_input,
            self.mensaje_error
        )

        # activamos de nuevo el botón
        self.btn_crear_grupos.disabled = False
        self.page.update()     

    async def cambiar_pestana(self, e):
        indice = e.control.selected_index # guardamos el indice del botón que se selecciona
        
        if indice == 0:
            await self.obtener_info_grupos()
            self.centro.content = ft.Row(
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    tarjeta_grupos(grupos, self.integrantes[i] if self.integrantes else ""),
                )
                for i, grupos in enumerate(self.datos_grupo or [])
            ],
        )
        elif indice == 1:
            # aqui el controlador de mapay agregamos al centro la vista del mapa
            print ("MAPA JAIME")
        elif indice == 2:
            wrapper = self.controlador.wrapper 
            controlador_u = UserController(self.page, wrapper) # MIRA MI COMENTARIO EN EL IMPORT
            self.centro.content = VistaPerfil(self.page, controlador_u).vista()

        self.page.update()     
    
    def vista(self):

        # Construir el contenido inicial del centro (grupos)
        contenido_centro = ft.Row(
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    tarjeta_grupos(grupos, self.integrantes[i] if self.integrantes else ""),
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
                    width=200,
                    content=ft.Column([
                        ft.Text("Bienvenido", size=20, weight="bold"),
                        self.nombre_grupo_input,
                        self.integrante_input,
                        self.btn_crear_grupos,
                        self.btn_eliminar_grupo,
                        self.btn_anyadir_integrante,
                    ], spacing=10),
                ),
                # Centro dinámico (expande para ocupar el espacio)
                ft.Container(expand=True, content=self.centro),
                # Barra de navegación inferior
                self.inferior,
            ],
            spacing=10,
        ),
    )