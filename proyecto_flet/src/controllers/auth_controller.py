import flet as ft
import asyncio

class AuthController:
    def __init__(self,page,wrapper, vista = None):
        self.page = page
        self.wrapper = wrapper
        self.vista = vista

    async def registrar_usuario (self,e):
        self.vista.mensaje_error.value = ""
        self.page.update()

        datos = [self.vista.nombre_input.value,self.vista.email_input.value,self.vista.psw_input.value,self.vista.psw_confirmar.value,self.vista.telefono_input.value]

        if not all (datos):
            self.vista.mensaje_error.value = "Todos los campos son obligatorios"
        elif self.vista.psw_input.value != self.vista.psw_confirmar.value:
            self.vista.mensaje_error.value = "Las contraseñas no coinciden"
            self.vista.psw_input.value = ""
            self.vista.psw_confirmar.value = ""
        elif "@" not in self.vista.email_input.value or "." not in self.vista.email_input.value:
            self.vista.mensaje_error.value = "Introduce un email válido"
        elif len(self.vista.psw_input.value) < 8:
                self.vista.mensaje_error.value = "La contraseña debe de tener mínimo 8 caracteres"
        else:
            registrado, aviso = await self.wrapper.registrarse(self.vista.nombre_input.value,self.vista.telefono_input.value,self.vista.email_input.value,self.vista.psw_input.value)
            if registrado:
                # provisional para confirmar en pantalla el registro
                self.vista.mensaje_error.value = "Usuario registrado correctamente, puedes iniciar sesión"
                self.vista.mensaje_error.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                await self.page.push_route("/")
                '''# uso de snack_bar para mostrar el aviso de registrado y que desaparezca solo NO ME APARECE
                self.page.snack_bar = ft.SnackBar(ft.Text("Registro completado correctamente, ya puedes iniciar sesion"))
                self.page.snack_bar.open = True'''
            else:
                error_registro = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "EMAIL_EXISTS" in error_registro:
                    self.vista.mensaje_error.value = "Correo ya registrado"
                elif "INVALID_EMAIL" in error_registro:
                    self.vista.mensaje_error.value = "No es un email valido"
                else:
                    self.vista.mensaje_error.value = "Error al registrar"

        # limpiamos el campo de la contraseña tras saltar un error
        self.vista.psw_input.value = ""
        self.vista.psw_confirmar.value = ""

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
