import flet as ft # type: ignore
import asyncio

class SettingsController:
    def __init__(self, page, ajustes_service, vista = None):
        self.page = page
        self.service = ajustes_service
        self.vista = vista

    # funcion para cambiar el tema de la aplicacion (claro/oscuro)
    async def tema (self,e):
        if self.page.theme_mode is None:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.Icons.DARK_MODE # el icono del boton es el del tema oscuro
            e.control.tooltip = "Cambiar tema a modo claro" # tooltip para indicar que si pulsamos sobre el icono se cambiara a tema claro
            await self.page.shared_preferences.set("tema","dark") # guardamos los cambios en el dispositivo
        elif self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.Icons.LIGHT_MODE # el icono del botón es el del tema claro
            e.control.tooltip = "Cambiar tema a modo oscuro" # tooltip para indicar que si pulsamos sobre el icono se cambiara a tema oscuro
            await self.page.shared_preferences.set("tema","light") # guardamos los cambios en el dispositivo
        e.control.update()
        self.page.update()
        print(f"Tema cambiado a: {self.page.theme_mode}")

        
    # funcion que muetra la tarjeta
    def mostrar_tarjeta_psw(self):
        self.vista.tarjeta_psw.visible = True
        self.page.update()

    # funcion que abre el componente CardPassword, valida los datos y llama al wrapper
    async def cambio_psw (self,componente):
        componente.mensaje_error.value = ""
        componente.mensaje_error.color = "red"
        componente.update()

        # validaciones para el cambio de contraseña
        if not componente.psw_nueva.value or not componente.psw_confirmar.value:
            componente.mensaje_error.value = "Todos los campos son obligatorios"
        elif componente.psw_nueva.value != componente.psw_confirmar.value:
            componente.mensaje_error.value = "Las contraseñas no coinciden"
        elif len(componente.psw_nueva.value) < 8:
            componente.mensaje_error.value = "La contraseña debe tener mínimo 8 caracteres"
        else:
            exito, aviso = await self.service.cambiar_psw(componente.psw_nueva.value)
            if exito:
                componente.mensaje_error.value = "Contraseña actualizada correctamente"
                componente.mensaje_error.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                await self.service.auth_s.cerrar_sesion() # si se ha cambiado la contraseña se cierra la sesion y pide que vuelvas a iniciar
                self.page.go("/")            
            else:
                error_psw = str(aviso).upper()
                if "WEAK_PASSWORD" in error_psw:
                    componente.mensaje_error.value = "La contraseña es muy débil"
                elif "REQUIRES_RECENT_LOGIN" in error_psw:
                    componente.mensaje_error.value = "Por seguridad, cierra sesión y vuelve a entrar"
                else:
                    componente.mensaje_error.value = "Error de conexión. Inténtalo de nuevo"

        # limpiamos los campos tras saltar el error
        componente.psw_nueva.value = ""
        componente.psw_confirmar.value = ""
        self.page.update()

    # funcion que abre un dialogo de confirmación para eliminar la cuenta
    async def dialogo(self, e):
        self.dialogo_confirmacion = ft.AlertDialog(
            modal=True, # Evita que se cierre haciendo clic fuera
            title=ft.Text("ELIMINAR CUENTA"),
            content=ft.Text("¿Deseas eliminar esta cuenta? Se eliminará toda la información."),
            actions=[
                ft.TextButton("CANCELAR", on_click=lambda _: self.cerrar_dialogo()),
                ft.ElevatedButton(
                    "BORRAR", 
                    on_click=self.borrar_cuenta, 
                    bgcolor="red", 
                    color="white"
                )
            ]
        )
        self.page.overlay.append(self.dialogo_confirmacion)
        # abrimos el dialogo
        self.dialogo_confirmacion.open=True
        self.page.update()
    # funcion para borrar la cuenta
    async def borrar_cuenta(self, e):
        exito, aviso = await self.service.borrar_cuenta()
        if exito:
            # recorremos el overlay para cerrar CUALQUIER diálogo abierto
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
                        ft.TextButton("ACEPTAR", on_click=lambda _: self.cerrar_dialogo())
                    ]
            
            self.page.update()
            print(f"Error al borrar: {aviso}")

    async def cerrar_sesion(self, e):
        await self.service.auth_s.cerrar_sesion()
        self.page.index_navegacion = 0 # reseteamos para que al volver a iniciar sesion aparezca grupos
        self.page.go("/") # abre el login una vez cerrada la sesión

    def cerrar_dialogo(self):
        for control in self.page.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        self.page.update()