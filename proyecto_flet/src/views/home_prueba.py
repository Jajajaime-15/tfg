import flet as ft
from views.perfil import VistaPerfil
from controllers.user_controller import UserController

class MainLayout: # EL NOMBRE DEL SCRIPT Y LA CLASE NO SE PARECEN EN NADA, HAY QUE ENCONTRAR UN PUNTO COMUN Y CAMBIAR UNO U OTRO
    def __init__(self, page, wrapper):
        self.page = page
        self.wrapper = wrapper
        self.controlador_u = UserController(self.page, self.wrapper) # POR QUE ESTE CONTROLADOR AQUI EN VEZ DE EN ROUTER? DEBERIA RECIBIRLO COMO PARAMETRO, NO? MIRA EN ROUTER.PY
        # SOBRE LA LINEA DE ARRIBA CREO QUE ACABO DE VER QUE EL PROBLEMA ES QUE EN ROUTER PASAS EL WRAPPER CUANDO YA TIENES ALLI EL USER Y PODRIAS PASARLO DIRECTAMENTE, NO?
        # Y ASI TE AHORRAS EL WRAPPER AQUI ADEMAS DEL USERCONTROLLER IMPORTADO
        self.centro = ft.Container(expand=True)
        # self.cargar_pestana_grupos()
        # guardamos el indice (en el caso de volver para atras desde ajustes voolvemos a home pero recordamos que estabamos en perfil)
        self.index_inicio = getattr(self.page,"index_navegacion",0) # NO SERIA MEJOR EN SHARED_PREFERENCES ESTO TMB?
        # barra de los botones de abajo con grupos,mapa y perfil
        self.inferior = ft.NavigationBar(
            selected_index=self.index_inicio, # recuperamos el indice
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
            # Vista de Mapa (Jaime) - Placeholder temporal
            self.centro.content = ft.Column([
                ft.Icon(ft.Icons.MAP_ROUNDED, size=50, color="grey"),
                ft.Text("MAPA EN DESARROLLO", size=20, weight="bold", color="grey")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        elif indice == 2:
            self.centro.content = VistaPerfil(self.page, self.controlador_u).vista()
        
        self.page.update()

    async def cambiar_pestana(self, e): # POR QUE ASYNC SI NO ES ASINCRONO? ES ALGO DE CARA AL FUTURO?
        indice = e.control.selected_index # guardamos el indice del botón que se selecciona
        
        if indice == 0:
            print ("GRUPOS JULIO")
        elif indice == 1:
            # aqui el controlador de mapay agregamos al centro la vista del mapa
            print ("MAPA JAIME")
        elif indice == 2:
            self.centro.content = VistaPerfil(self.page, self.controlador_u).vista()
        
        self.page.update()

    def vista(self):
        return ft.Column([
            self.centro,
            self.inferior
        ], expand=True)