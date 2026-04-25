import flet as ft
from flet import TextField
from components.components import tarjeta_grupos
from views.perfil_view import VistaPerfil


class VistaGrupos:
    def __init__(self, page, group_controller, user_controller):
        self.page = page
        self.group_controller = group_controller # guardamos el controlador de grupos para usar sus funciones
        self.user_controller = user_controller # guardamos el controlador de user para usar sus funciones
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

    def manejador_tarjeta(self, grupo_nombre):
        async def manejador(e):
            await self.anyadir_integrante(grupo_seleccionado=grupo_nombre)
            print(f"Tarjeta seleccionada: {grupo_nombre}")
            # Aquí puedo añadir acciones del grupo seleccionado
            self.grupo_seleccionado = grupo_nombre
            self.nombre_grupo_input.value = grupo_nombre
            self.page.update()
        return manejador    

    async def crear_grupo(self, e):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()

        # llamamos a la función para crear un grupo
        await self.group_controller.crear_grupo(
            self.nombre_grupo_input,
            self.integrante_input,
            self.mensaje_error
        )
    
    async def obtener_info_grupos(self):

        # llamamos a la función para crear un grupo
        
        self.datos_grupo, self.integrantes = await self.group_controller.mostrar_grupos(
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
        await self.group_controller.eliminar_grupo(
            self.nombre_grupo_input,
            self.mensaje_error
        )

        # activamos de nuevo el botón
        self.btn_crear_grupos.disabled = False
        self.page.update()        

    async def anyadir_integrante(self, grupo_seleccionado=None):
        # botón desactivado para no hacer más de un click y no bloquear la conexión con firebase
        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = "" # el mensaje de error lo dejamos vacío
        self.page.update()
        # llamamos a la función para añadir un integrante a un grupo
        await self.group_controller.anyadir_participante(
            grupo_seleccionado,
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
                    tarjeta_grupos(grupos, self.integrantes[i] if self.integrantes else "", on_click_tarjeta=self.manejador_tarjeta(grupos)),
                )
                for i, grupos in enumerate(self.datos_grupo or [])
            ],
        )
        elif indice == 1:
            # aqui el controlador de mapay agregamos al centro la vista del mapa
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
                    tarjeta_grupos(grupos, self.integrantes[i] if self.integrantes else "", on_click_tarjeta=self.manejador_tarjeta(grupos)),
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
                    self.nombre_grupo_input,
                    self.btn_crear_grupos,
                ),
                # Centro dinámico (expande para ocupar el espacio)
                ft.Container(expand=True, content=self.centro),
                # Barra de navegación inferior
                self.inferior,
            ],
            spacing=10,
        ),
    )