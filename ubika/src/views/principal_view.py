import flet as ft
from views.perfil_view import VistaPerfil
from views.mapa_view import VistaMapa

class VistaPrincipal: 
    def __init__(self, page, controlador_user, controlador_mapa):
        self.page = page
        self.controlador_u = controlador_user
        self.controlador_mapa = controlador_mapa
        self.centro = ft.Container(expand=True)
        # self.cargar_pestana_grupos()
        # guardamos el indice (en el caso de volver para atras desde ajustes volvemos a home pero recordamos que estabamos en perfil)
        self.index_inicio = getattr(self.page, "index_navegacion", 0)
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
        if indice == 0: # grupos
            pass # Vista de Grupos (Julio)
        elif indice == 1: # mapa
            nueva_vista = VistaMapa(self.page, self.controlador_mapa)
            self.centro.content = nueva_vista.vista()
            self.page.run_task(self.controlador_mapa.iniciar_gps())
        elif indice == 2: # perfil
            nueva_vista = VistaPerfil(self.page, self.controlador_u)
            self.centro.content = nueva_vista.vista()
            self.page.run_task(self.controlador_u.cargar_perfil())
        self.page.update()

    def cambiar_pestana(self, e):
        indice = e.control.selected_index  # guardamos el indice del botón que se selecciona
        if indice == 0: # grupos
            print("GRUPOS JULIO")
        elif indice == 1: # mapa
            nueva_vista = VistaMapa(self.page, self.controlador_mapa)
            self.centro.content = nueva_vista.vista()
            self.page.run_task(self.controlador_mapa.iniciar_gps())
        elif indice == 2: # perfil
            nueva_vista = VistaPerfil(self.page, self.controlador_u)
            self.centro.content = nueva_vista.vista()
            self.page.run_task(self.controlador_u.cargar_perfil())
        self.page.update()

    def vista(self):
        return ft.Column([
            self.centro,
            self.inferior
        ], expand=True)
