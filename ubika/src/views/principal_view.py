import flet as ft
from views.perfil_view import VistaPerfil
from views.mapa_view import VistaMapa

class VistaPrincipal: 
    def __init__(self, page, controlador_user, controlador_mapa):
        self.page = page
        self.controlador_user = controlador_user
        self.controlador_mapa = controlador_mapa
        self.centro = ft.Container(expand=True)
        # guardamos el indice (en el caso de volver para atras desde ajustes volvemos a home pero recordamos que estabamos en perfil)
        self.index_inicio = getattr(self.page, "index_navegacion", 0)
        self.vista_mapa = VistaMapa(self.page, self.controlador_mapa)
        self.vista_perfil = None
        
        self.inferior = ft.NavigationBar( # barra de navegacion de los botones de abajo con grupos, mapa y perfil
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
        self.actualizar_vista(self.index_inicio)

    # funcion para que cuando volvamos hacia atras recuerde en que vista estabamos
    def actualizar_vista(self, indice):
        if indice == 0: # grupos
            pass # Vista de Grupos (Julio)
        elif indice == 1: # mapa
            self.centro.content = self.vista_mapa.vista()
        elif indice == 2: # perfil
            if not self.vista_perfil: # la primera vez que se abre
                self.vista_perfil = VistaPerfil(self.page, self.controlador_user)

            self.centro.content = self.vista_perfil.vista()
            self.controlador_user.limpiar_vista() # limpiamos la vista de los datos anteriores
            self.page.run_task(self.controlador_user.cargar_perfil) # cargamos el perfil que ademas sincroniza los datos

        self.page.update()

    def cambiar_pestana(self, e):
        indice = e.control.selected_index  # guardamos el indice del botón que se selecciona
        self.actualizar_vista(indice)

    def vista(self):
        return ft.Column([
            self.centro,
            self.inferior
        ], expand=True)
