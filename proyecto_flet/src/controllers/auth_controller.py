import flet as ft
import asyncio

class AuthController:
    def __init__(self,page,wrapper):
        self.page = page
        self.wrapper = wrapper

    async def registrar_usuario (self,nombre,email,psw,psw_conf,telefono,mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre.value,email.value,psw.value,psw_conf.value,telefono.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
        elif psw.value != psw_conf.value:
            mensaje.value = "Las contraseñas no coinciden"
            psw.value = ""
            psw_conf.value = ""
        elif "@" not in email.value or "." not in email.value:
            mensaje.value = "Introduce un email válido"
        elif len(psw.value) < 8:
                mensaje.value = "La contraseña debe de tener mínimo 8 caracteres"
        else:
            registrado, aviso = await self.wrapper.registrarse(nombre.value,telefono.value,email.value,psw.value)
            if registrado:
                # provisional para confirmar en pantalla el registro
                mensaje.value = "Usuario registrado correctamente, puedes iniciar sesión"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                await self.page.push_route("/")
                '''# uso de snack_bar para mostrar el aviso de registrado y que desaparezca solo NO ME APARECE
                self.page.snack_bar = ft.SnackBar(ft.Text("Registro completado correctamente, ya puedes iniciar sesion"))
                self.page.snack_bar.open = True'''
            else:
                error_registro = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "EMAIL_EXISTS" in error_registro:
                    mensaje.value = "Correo ya registrado"
                elif "INVALID_EMAIL" in error_registro:
                    mensaje.value = "No es un email valido"
                else:
                    mensaje.value = "Error al registrar"

        # limpiamos el campo de la contraseña tras saltar un error
        psw.value = ""
        psw_conf.value = ""

        self.page.update()

    async def conectarse (self,email,psw,mensaje):
        mensaje.value = ""
        self.page.update()

        if not email.value or not psw.value:
            mensaje.value = "Introduce email y contraseña"
        else:
            conectado, aviso = await self.wrapper.iniciar_sesion(email.value,psw.value)
            if conectado:
                # provisional para confirmar en pantalla el inicio de sesion
                mensaje.value = "Sesión iniciada"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)                
                await self.page.push_route("/") # ruta a la pantalla principal/perfil/grupos
                '''self.page.snack_bar = ft.SnackBar(ft.Text("Sesión iniciada"))
                self.page.snack_bar.open = True
                self.page.update()'''
            else:
                error_log = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "INVALID_LOGIN_CREDENTIALS" in error_log or "INVALID_PASSWORD" in error_log:
                    mensaje.value = "Email o contraseña incorrecto"
                elif "USER_NOT_FOUND" in error_log:
                    mensaje.value = "Usuario no encontrado"
                elif "TOO_MANY_ATTEMPTS" in error_log:
                    mensaje.value = "Demasiados intentos, intentalo más tarde"
                else:
                    mensaje.value = "Error al conectarse"
                    
                # limpiamos el campo de la contraseña y dejamos el focus ahí tras saltar un error    
                psw.value = ""
                psw.focus()

        self.page.update()

    async def recuperar_psw(self,email,mensaje):
        mensaje.value = ""
        self.page.update()

        if not email.value:
            mensaje.value = "Introduce el email de tu cuenta para recuperarla"
        else:
            enviado, aviso = await self.wrapper.recu_psw(email.value)
            if enviado:
                # provisional para confirmar en pantalla correo enviado para recuperar contraseña
                mensaje.value = "Correo enviado"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)    
                await self.page.push_route("/")
                '''self.page.snack_bar = ft.SnackBar(ft.Text("Correo enviado"))
                self.page.snack_bar.open = True
                self.page.update()'''
            else:
                error_recu = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "NOT_FOUND" in error_recu:
                    mensaje.value = "No hay ninguna cuenta con ese email"
                elif "INVALID_EMAIL" in error_recu:
                    mensaje.value = "No es un email valido"
                else:
                    mensaje.value = "Error al procesar la solicitud"
                
        self.page.update()

    async def crear_grupo (self,nombre,mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
        else:
            creado, aviso = await self.wrapper.crear_grupo(nombre.value)
            if creado:
                # provisional para confirmar en pantalla el registro
                mensaje.value = "Grupo creado correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                await self.page.push_route("/")
                '''# uso de snack_bar para mostrar el aviso de registrado y que desaparezca solo NO ME APARECE
                self.page.snack_bar = ft.SnackBar(ft.Text("Grupo creado correctamente"))
                self.page.snack_bar.open = True'''
            else:
                mensaje.value = f"Error al crear grupo: {aviso}"
                mensaje.color = "red"


        self.page.update()

    async def eliminar_grupo (self,nombre,mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
        else:
            borrado, aviso = await self.wrapper.eliminar_grupo(nombre.value)
            if borrado:
                # provisional para confirmar en pantalla el registro
                mensaje.value = "Grupo eliminado correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                await self.page.push_route("/")
                '''# uso de snack_bar para mostrar el aviso de registrado y que desaparezca solo NO ME APARECE
                self.page.snack_bar = ft.SnackBar(ft.Text("Grupo creado correctamente"))
                self.page.snack_bar.open = True'''
            else:
                mensaje.value = f"Error al crear grupo: {aviso}"
                mensaje.color = "red"


        self.page.update()    