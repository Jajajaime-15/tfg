import flet as ft # type: ignore
import asyncio
import json
from utils.mostrar_avisos import mostrar_aviso

class AjustesController:
    def __init__(self, page, ajustes_service, usuario_service, vista = None):
        self.page = page
        self.service = ajustes_service
        self.usuario_s = usuario_service
        self.vista = vista

    # funcion para cambiar el tema de la aplicacion (claro/oscuro)
    async def tema(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT or self.page.theme_mode is None:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.Icons.DARK_MODE # el icono del boton es el del tema oscuro
            e.control.tooltip = "Cambiar tema a modo claro" # tooltip para indicar que si pulsamos sobre el icono se cambiara a tema claro
            await self.page.shared_preferences.set("tema","dark") # guardamos los cambios en el dispositivo
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.Icons.LIGHT_MODE # el icono del botón es el del tema claro
            e.control.tooltip = "Cambiar tema a modo oscuro" # tooltip para indicar que si pulsamos sobre el icono se cambiara a tema oscuro
            await self.page.shared_preferences.set("tema","light") # guardamos los cambios en el dispositivo
        
        e.control.update() # se actualiza el boton
        self.page.update()

    # funcion que abre el componente CardPassword, valida los datos y llama al wrapper
    async def cambio_psw(self, componente):
        mostrar_aviso(self.page, componente,"")
        componente.update()

        # validaciones para el cambio de contraseña
        if not componente.psw_nueva.value or not componente.psw_confirmar.value:
            mostrar_aviso(self.page, componente,"Todos los campos son obligatorios")
        elif componente.psw_nueva.value != componente.psw_confirmar.value:
            mostrar_aviso(self.page, componente,"Las contraseñas no coinciden")
        elif len(componente.psw_nueva.value) < 8:
            mostrar_aviso(self.page, componente,"La contraseña debe tener mínimo 8 caracteres")
        else:
            exito, aviso = await self.service.cambiar_psw(componente.psw_nueva.value)
            if exito:
                mostrar_aviso(self.page, componente,"Contraseña actualizada. Inicie sesión de nuevo", color="#1A6AFE")
                self.page.update()
                await asyncio.sleep(2)
                await self.cerrar_sesion(None) # si se ha cambiado la contraseña se cierra la sesion y pide que vuelvas a iniciar
                self.page.go("/")            
            else:
                error_psw = str(aviso).upper()
                if "WEAK_PASSWORD" in error_psw:
                    mostrar_aviso(self.page, componente,"La contraseña es muy débil")
                elif "REQUIRES_RECENT_LOGIN" in error_psw:
                    mostrar_aviso(self.page, componente,"Por seguridad, cierra sesión y vuelve a entrar")
                else:
                    mostrar_aviso(self.page, componente,"Error de conexión. Vuelve a iniciar sesión")

        # limpiamos los campos tras saltar el error
        componente.psw_nueva.value = ""
        componente.psw_confirmar.value = ""
        self.page.update()

    # funcion para borrar la cuenta
    async def borrar_cuenta(self, e):
        exito, aviso = await self.service.borrar_cuenta()
        if exito:
            # limpiamos lo guardado en memoria
            self.usuario_s.id_usuario = None
            self.usuario_s.token = None
            self.service.id_usuario = None
            self.service.token = None
            self.page.router.reset_vistas() # llamamos a la funcion que resetea la vista
            # recorremos el overlay para cerrar cualquier diálogo abierto
            for control in self.page.overlay:
                if isinstance(control,ft.AlertDialog):
                    control.open=False
            self.page.update()
            await asyncio.sleep(0.5)
            # una vez eliminada la cuenta volvemos al login
            self.page.go("/") 
        else:
            error_exito = str(aviso).upper()
            for control in self.page.overlay:
                if isinstance(control, ft.AlertDialog):
                    if "CREDENTIAL_TOO_OLD" in error_exito or "SENSITIVE" in error_exito:
                        control.title = ft.Text("ACCIÓN DENEGADA", color="red")
                        control.content = ft.Text("Por seguridad, debes cerrar sesión y volver a entrar antes de eliminar tu cuenta.")
                    else:
                        control.content = ft.Text("No se pudo eliminar la cuenta. Inténtalo más tarde.")
                    # Cambiamos el botón a ACEPTAR
                    control.actions = [
                        ft.TextButton("ACEPTAR", 
                                    on_click=lambda _: self.cerrar_dialogo())
                    ]
            self.page.update()

    async def cerrar_sesion(self, e):
        await self.service.auth_s.cerrar_sesion() # cerramos la sesion con firebase

        self.usuario_s.id_usuario = None
        self.usuario_s.token = None
        self.service.id_usuario = None
        self.service.token = None

        self.page.router.reset_vistas() # llamamos a la funcion que resetea la vista

        self.page.index_navegacion = 0 # reseteamos para que al volver a iniciar sesion aparezca grupos
        self.page.go("/") # abre el login una vez cerrada la sesión

    # funcion para activar o desactivar la ubicacion del usuario
    async def compartir_ubicacion(self, e):
        # si no es un dispositivo móvil no hacemos nada
        if self.page.platform != ft.PagePlatform.ANDROID:
            return

        # vemos lo que está seleccionado en el switch (activo/inactivo) y lo guardamos
        nuevo_estado = self.vista.ubicacion.value # aqui nos indica True o False
        estado = "true" if nuevo_estado else "false" # el estado hay que convertirlo a texto para guardarlo en shared preferences que no admite booleanos
        datos = {"compartir_ubicacion":estado}
        exito, aviso = await self.usuario_s.actualizar_datos(datos)
        if exito:
            id_user = await self.page.shared_preferences.get("id_usuario")
            token = await self.page.shared_preferences.get("token")
            if not nuevo_estado:
                try:
                    grupos_guardados = await self.page.shared_preferences.get("grupos")
                    grupos = json.loads(grupos_guardados) if grupos_guardados else {}
                    if grupos:
                        for id_grupo in grupos.keys():
                            self.usuario_s.db.child("ubicaciones").child(id_grupo).child(id_user).remove(token)
                        print("Ubicación desactivada en todos los grupos")
                    else:
                        print("Ubicación desactivada")
                except Exception as ex:
                    print(f"Error al desactivar la ubicación: {ex}")
            else:
                print ("Ubicación activada")
        else:
            print(f"Error al sincronizar con firebase: {estado}")
        self.page.update()

    # funcion para que al cerrar sesion el switch de la ubicación no se reinicie y se mantenga lo seleccionado, tambien carga el tema
    async def cargar_ajustes(self):
        if self.vista: # comprobacion de que la vista existe para evitar errores
            # comprobamos el tema que tiene y lo cargamos
            if self.page.theme_mode == ft.ThemeMode.DARK:
                self.vista.btn_tema.icon = ft.Icons.DARK_MODE
                self.vista.btn_tema.tooltip = "Cambiar tema a modo claro"
            else:
                self.vista.btn_tema.icon = ft.Icons.LIGHT_MODE
                self.vista.btn_tema.tooltip = "Cambiar tema a modo oscuro"

            # comprobamos si estamos en windows o en movil
            android = self.page.platform == ft.PagePlatform.ANDROID
            if android == False: # si no estamos en movil
                self.vista.ubicacion.disabled = True # bloqueamos el switch
                self.vista.ubicacion.value = False 
            else:
                self.vista.ubicacion.disabled = False
                # comprobamos el estado de la ubicacion y lo cargamos
                estado = await self.page.shared_preferences.get("compartir_ubicacion")
                estado_guardado = str(estado).lower().strip()

                # volvemos a convertir el estado a un booleano para el switch
                if estado_guardado == "true":
                    self.vista.ubicacion.value = True
                else:
                    self.vista.ubicacion.value = False

            self.vista.btn_tema.update()
            self.vista.ubicacion.update() # obligamos a que se active/desactive el switch según la configuración guardada en la última sesión
            self.page.update()