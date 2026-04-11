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
                return
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

    async def conectarse (self,e):
        self.vista.mensaje_error.value = ""
        self.page.update()

        if not self.vista.email_input.value or not self.vista.psw_input.value:
            self.vista.mensaje_error.value = "Introduce email y contraseña"
        else:
            conectado, aviso = await self.wrapper.iniciar_sesion(self.vista.email_input.value,self.vista.psw_input.value)
            if conectado:
                # provisional para confirmar en pantalla el inicio de sesion
                self.vista.mensaje_error.value = "Sesión iniciada"
                self.vista.mensaje_error.color = "green"
                self.page.update()
                await asyncio.sleep(2)                
                await self.page.push_route("/home") # ruta a la pantalla principal/perfil/grupos
            else:
                error_log = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "INVALID_LOGIN_CREDENTIALS" in error_log or "INVALID_PASSWORD" in error_log:
                    self.vista.mensaje_error.value = "Email o contraseña incorrecto"
                elif "USER_NOT_FOUND" in error_log:
                    self.vista.mensaje_error.value = "Usuario no encontrado"
                elif "TOO_MANY_ATTEMPTS" in error_log:
                    self.vista.mensaje_error.value = "Demasiados intentos, intentalo más tarde"
                else:
                    self.vista.mensaje_error.value = "Error al conectarse"
                    
                # limpiamos el campo de la contraseña y dejamos el focus ahí tras saltar un error    
                self.vista.psw_input.value = ""
                self.vista.psw_input.focus()

        self.page.update()

    async def recuperar_psw(self,e):
        self.vista.mensaje_error.value = ""
        self.page.update()

        if not self.vista.email_input.value:
            self.vista.mensaje_error.value = "Introduce el email de tu cuenta para recuperarla"
        else:
            enviado, aviso = await self.wrapper.recu_psw(self.vista.email_input.value)
            if enviado:
                # provisional para confirmar en pantalla correo enviado para recuperar contraseña
                self.vista.mensaje_error.value = "Correo enviado"
                self.vista.mensaje_error.color = "green"
                self.page.update()
                await asyncio.sleep(2)    
                await self.page.push_route("/")
            else:
                error_recu = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "NOT_FOUND" in error_recu:
                    self.vista.mensaje_error.value = "No hay ninguna cuenta con ese email"
                elif "INVALID_EMAIL" in error_recu:
                    self.vista.mensaje_error.value = "No es un email valido"
                else:
                    self.vista.mensaje_error.value = "Error al procesar la solicitud"
                
        self.page.update()
