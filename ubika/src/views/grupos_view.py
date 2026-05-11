import flet as ft # type: ignore
from components.tarjeta_grupos import TarjetaGrupo
from components.boton_principal import BotonPrincipal
from components.titulos import TituloSeccion
import asyncio

class VistaGrupos:
    def __init__(self, page, grupos_controller):
        self.page = page
        self.grupos_controller = grupos_controller # guardamos el controlador de grupos para usar sus funciones
        self.datos_grupo = None
        self.integrantes = None
        self.emails = None
        self.centro = ft.Container(expand=True)
        self.grupos_controller.vista = self # vinculamos la vista con el controller

        self.btn_crear_grupos = BotonPrincipal(
            texto="Añadir grupo",
            icono=ft.Icons.ADD,
            ancho=200,
            accion=self.crear_grupo
        )

        self.mensaje_error = ft.Text(value="", color="red", weight="bold", visible=False)

    def manejador_tarjeta(self, grupo_nombre):
        async def manejador(e):
            self.grupo_seleccionado = grupo_nombre # Seleccionar el grupo para operaciones mas adelante como eliminar o actualizar el nombre
            self.page.update()
        return manejador    

    async def crear_grupo(self, e):
        await self.page.push_route("/crear_grupo")

    async def obtener_info_grupos(self):
        self.datos_grupo, self.integrantes, self.emails, self.ids_admins = await self.grupos_controller.mostrar_grupos(self.mensaje_error)
        self.btn_crear_grupos.disabled = False # activamos de nuevo el botón
        self.page.update()    

    def eliminar_integrante_desde_tarjeta(self, e, nombre_grupo, email_integrante):
        print(f"Eliminando integrante: {email_integrante} del grupo: {nombre_grupo}")

        self.btn_crear_grupos.disabled = True
        self.mensaje_error.value = ""
        self.page.update()

        # creamos un proceso asíncrono para la eliminacion
        async def eliminacion():
            exito = await self.grupos_controller.eliminar_participante(nombre_grupo, email_integrante,self.mensaje_error) # llamamos al controlador para realizar el borrado del miembro
            if not exito: # si no se realiza nada
                await asyncio.sleep(2)

            await self.actualizar_tarjetas_grupos() # volvemos a cargar las tarjetas de los grupos
            self.btn_crear_grupos.disabled = False
            self.page.update()

        self.page.run_task(eliminacion) 

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

    def agregar_integrante_desde_tarjeta(self, nombre_grupo, integrante_field):
        # Funcion para manejar el click en el botón agregar desde la tarjeta del grupo
        nombre_integrante = integrante_field.value # Extraer el valor del TextField

        # Validar que no esté vacío
        if not nombre_integrante or nombre_integrante.strip() == "":
            integrante_field.error_text = "Email obligatorio"
            self.page.update()
            return

        # Limpiar errores y el valor del TextField para la proxima vez
        integrante_field.error_text = None
        integrante_field.value = ""

        self.page.run_task(
            self.grupos_controller.agregar_participante,
            nombre_grupo,
            nombre_integrante,
            self.mensaje_error
        )

    async def actualizar_tarjetas_grupos(self):
        await self.obtener_info_grupos()
        self.centro.content = self.generar_fila_grupos() # refrescamos el contenido del centro
        self.page.update()

    # funcion que crea la fila horizontal de las tarjetas de grupos
    def generar_fila_grupos(self):
        return ft.Row(
            expand=True,
            spacing=20,
            scroll=ft.ScrollMode.ADAPTIVE,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                TarjetaGrupo(
                    nombre_grupo=grupo,
                    id_usuario=self.grupos_controller.obtener_id(),
                    id_admin_grupo=self.ids_admins[i] if self.ids_admins and i < len(self.ids_admins) else None, 
                    miembros=self.integrantes[i] if self.integrantes and i < len(self.integrantes) else [], 
                    emails=self.emails[i] if self.emails and i < len(self.emails) else [],
                    on_agregar=self.agregar_integrante_desde_tarjeta,
                    on_eliminar=self.eliminar_grupo_desde_tarjeta,
                    on_editar=self.editar_grupo_desde_tarjeta,
                    on_abandonar = self.abandonar_grupo,
                    on_eliminar_integrante=self.eliminar_integrante_desde_tarjeta,
                    on_click_tarjeta=self.manejador_tarjeta(grupo)
                )
                for i, grupo in enumerate(self.datos_grupo or [])
            ],
        )

    def abandonar_grupo(self, grupo):
        self.mensaje_error.value = ""
        self.page.update()

        async def salir():
            await self.grupos_controller.abandonar_grupo (grupo, self.mensaje_error)
            await self.actualizar_tarjetas_grupos()
            self.page.update()

        self.page.run_task(salir)

    def vista(self):
        self.centro.content = self.generar_fila_grupos() 
        self.centro.alignment = ft.Alignment(0, 0)
        return ft.Container(
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Row([
                        TituloSeccion(texto="MIS GRUPOS", color="", tamanio=25),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(height=5, color="transparent"),

                    ft.Row([
                        self.btn_crear_grupos
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(height=20, color="transparent"), 
                    self.mensaje_error,

                    ft.Container(
                        content=self.centro,
                        padding=ft.Padding.symmetric(vertical=10),
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            )
        )