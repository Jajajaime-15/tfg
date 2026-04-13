import flet as ft
from views.perfil import VistaPerfil
from views.groups import VistaGrupos # llamas a la vista de grupos
from controllers.user_controller import UserController
from controllers.group_controller import GroupController # llamas al controlador de grupos

class MainLayout:
    def __init__(self, page, wrapper):
        self.page = page
        self.wrapper = wrapper
        self.centro = ft.Container(expand=True)
        self.cargar_pestana_grupos()

        # barra de los botones de abajo con grupos,mapa y perfil
        self.inferior = ft.NavigationBar(
            selected_index=0,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Grupos"),
                ft.NavigationBarDestination(icon=ft.Icons.MAP_OUTLINED, label="Mapa"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINED, label="Perfil"),
            ],
            on_change=self.cambiar_pestana
        )

    def mostrar_grupos(self):
        # aqui el controlador de grupos y agregamos al centro la vista de grupos
        controlador_g = GroupController(self.page, self.wrapper)
        self.centro.content = VistaGrupos(self.page, controlador_g).vista()

    async def cambiar_pestana(self, e):
        indice = e.control.selected_index # guardamos el indice del botón que se selecciona
        
        if indice == 0:
            self.mostrar_grupos()
        elif indice == 1:
            # aqui el controlador de mapay agregamos al centro la vista del mapa
            print ("MAPA JAIME")
        elif indice == 2:
            controlador_u = UserController(self.page, self.wrapper)
            self.centro.content = VistaPerfil(self.page, controlador_u).vista()

        self.page.update()

    def vista(self):
        return ft.Column([
            self.centro,
            self.inferior
        ], expand=True)