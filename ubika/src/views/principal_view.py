import flet as ft # type: ignore
import asyncio
from views.perfil_view import VistaPerfil
from controllers.usuario_controller import UsuarioController

class VistaPrincipal: 
    def __init__(self, page, user_controller):
        self.page = page
        self.controlador_u = user_controller
        self.centro = ft.Container(expand=True)
        # self.cargar_pestana_grupos()
        # guardamos el indice (en el caso de volver para atras desde ajustes voolvemos a home pero recordamos que estabamos en perfil)
        self.index_inicio = getattr(self.page, "index_navegacion", 0)  # Considera usar shared_preferences para persistencia
        # barra de los botones de abajo con grupos,mapa y perfil
        self.inferior = ft.NavigationBar(
            selected_index=self.index_inicio,  # recuperamos el indice
            bgcolor=ft.Colors.TRANSPARENT, # fondo transparente
            elevation=0, # quitamos la elevacion para que no haya sombras ni lineas
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Grupos"),
                ft.NavigationBarDestination(icon=ft.Icons.MAP_OUTLINED, label="Mapa"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINED, label="Perfil"),
            ],
            on_change=self.cambiar_pestana
        )
        # self.mostrar_grupos() # cargamos la pestaña inicial que es grupos
        self.actualizar_vista_centro(self.index_inicio)

    # funcion para que cuando volvamos hacia atras recuerde en que vista estabamos
    def actualizar_vista_centro(self, indice):
        if indice == 0:
            pass
            # Vista de Grupos (Julio)
        elif indice == 1:
            # Vista de Mapa (Jaime)
            self.centro.content = ft.Column([
                ft.Icon(ft.Icons.MAP_ROUNDED, size=50, color="grey"),
                ft.Text("MAPA EN DESARROLLO", size=20, weight="bold", color="grey")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        elif indice == 2:
            nueva_vista = VistaPerfil(self.page, self.controlador_u)
            self.centro.content = nueva_vista.vista()
            asyncio.create_task(self.controlador_u.cargar_perfil())
        self.page.update()

    def cambiar_pestana(self, e):
        indice = e.control.selected_index  # guardamos el indice del botón que se selecciona
        if indice == 0:
            print("GRUPOS JULIO")
        elif indice == 1:
            print("MAPA JAIME")
        elif indice == 2:
            nueva_vista = VistaPerfil(self.page, self.controlador_u)
            self.centro.content = nueva_vista.vista()
            asyncio.create_task(self.controlador_u.cargar_perfil())
        self.page.update()

    def vista(self):
        return ft.Column([
            self.centro,
            self.inferior
        ], expand=True)
