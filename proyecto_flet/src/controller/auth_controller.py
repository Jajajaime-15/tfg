import flet as ft

class AuthController:
    def __init__(self,page,wrapper):
        self.page = page
        self.wrapper = wrapper

    async def registrar_usuario (self,nombre,email,psw, telefono,mensaje):
        datos = [nombre.value,email.value,psw.value,telefono.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
        elif "@" not in email.value or "." not in email.value:
            mensaje.value = "Introduce un email válido"
        elif len(psw.value) < 8:
                mensaje.value = "La contraseña debe de tener mínimo 8 caracteres"
        else:
            registrado, aviso = await self.wrapper.registrarse(nombre.value,telefono.value,email.value,psw.value)
            if registrado:
                # uso de snack_bar para mostrar el aviso de registrado abajo en negro y desaparece solo
                self.page.snack_bar = ft.SnackBar(ft.Text("Registro completado correctamente"))
                self.page.snack_bar.open = True
                await self.page.go_async("/") # parte de Julio para el cambio de pantalla a 'login'
            else:
                mensaje.value = aviso

        await self.page.update_async()

    async def conectarse (self,email,psw,mensaje):
        if not email.value or not psw.value:
            mensaje.value = "Introduce email y contraseña"
        else:
            conectado, aviso = await self.wrapper.iniciar_sesion(email.value,psw.value)
            if conectado:
                self.page.snack_bar = ft.SnackBar(ft.Text("Sesión iniciada"))
                self.page.snack_bar.open = True
                await self.page.go_async("/")# parte de Julio para el cambio de pantalla al perfil de usuaio/mapa
            else:
                mensaje.value = aviso

        await self.page.update_async()