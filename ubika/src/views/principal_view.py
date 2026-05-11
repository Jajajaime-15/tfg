import flet as ft # type: ignore
from views.perfil_view import VistaPerfil
from views.mapa_view import VistaMapa
from views.grupos_view import VistaGrupos

class VistaPrincipal: 
    def __init__(self, page, controlador_usuario, controlador_mapa, controlador_grupos):
        self.page = page
        self.controlador_usuario = controlador_usuario
        self.controlador_mapa = controlador_mapa
        self.controlador_grupos = controlador_grupos

        self.centro = ft.Container( # el contenedor del centro lo ajustamos para que no quede pegado arriba del todo
            expand=True, 
            padding=ft.Padding.only(top=45, left=0, right=0, bottom=0)
        )

        self.index_inicio = getattr(self.page, "index_navegacion", 0) # guardamos el indice (en el caso de volver para atras desde ajustes volvemos a home pero recordamos que estabamos en perfil)

        self.vista_mapa = VistaMapa(self.page, self.controlador_mapa) # para que el mapa cargue desde la apertura de la vista principal de navegacion
        self.vista_perfil = None # dejamos en None para que solo esté en memoria cuando se entre en perfil
        self.vista_grupos = None # dejamos en None para que solo esté en memoria cuando se entre en grupos

        self.inferior = ft.NavigationBar( # barra de navegacion de los botones de abajo con grupos (home), mapa y perfil
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

        self.actualizar_vista(self.index_inicio)

    # funcion para que cuando volvamos hacia atras recuerde en que vista estabamos
    def actualizar_vista(self, indice):
        if indice == 0: # grupos
            if not self.vista_grupos: # la primera vez que se abre
                self.vista_grupos = VistaGrupos(self.page, self.controlador_grupos)
            self.centro.content = self.vista_grupos.vista()
            self.page.run_task(self.vista_grupos.actualizar_tarjetas_grupos)
        elif indice == 1: # mapa
            self.centro.content = self.vista_mapa.vista()
        elif indice == 2: # perfil
            if not self.vista_perfil: # la primera vez que se abre
                self.vista_perfil = VistaPerfil(self.page, self.controlador_usuario)
            self.centro.content = self.vista_perfil.vista()
            self.page.run_task(self.controlador_usuario.cargar_perfil) # cargamos el perfil que ademas sincroniza los datos

        self.page.update()

    def cambiar_pestana(self, e):
        indice = e.control.selected_index  # guardamos el indice del botón que se selecciona
        self.actualizar_vista(indice)

    def vista(self):
        return ft.Column([
            self.centro,
            self.inferior
        ], expand=True)