import asyncio
from utils.mostrar_avisos import mostrar_aviso

class AuthController:
    def __init__(self, page, auth_service, vista = None):
        self.page = page
        self.service = auth_service
        self.vista = vista

    async def registrar_usuario(self, e):
        mostrar_aviso(self.page, self.vista,"")
        self.page.update()

        # almacenamos todos los datos en una lista para despues poder comprobar
        datos = [self.vista.nombre_input.value,
                self.vista.email_input.value,
                self.vista.psw_input.value,
                self.vista.psw_confirmar.value,
                self.vista.telefono_input.value]

        # comprobamos que estén todos los campos rellenos 
        if not all (datos): # el all nos ayuda a comprobar todos los campos en vez de ir uno a uno
            mostrar_aviso(self.page, self.vista,"Todos los campos son obligatorios")
        elif self.vista.psw_input.value != self.vista.psw_confirmar.value:
            mostrar_aviso (self.page, self.vista,"Las contraseñas no coinciden")
            self.vista.psw_confirmar.value = ""
            await self.vista.psw_confirmar.focus()
        elif "@" not in self.vista.email_input.value or "." not in self.vista.email_input.value:
            mostrar_aviso(self.page, self.vista,"Introduce un email válido")
        elif len(self.vista.psw_input.value) < 8:
            mostrar_aviso(self.page, self.vista,"La contraseña debe de tener mínimo 8 caracteres")
        else:
            registrado, aviso = await self.service.registrarse(self.vista.nombre_input.value,self.vista.telefono_input.value,
                                                            self.vista.email_input.value,self.vista.psw_input.value)
            if registrado:
                mostrar_aviso(self.page, self.vista,"Usuario registrado", color="#1A6AFE")
                self.page.update()
                await asyncio.sleep(1.5) # damos un tiempo para que el usuario lea el mensaje andes de redireccionar al login
                self.page.go("/")
            else:
                error_registro = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "EMAIL_EXISTS" in error_registro:
                    mostrar_aviso(self.page, self.vista,"Correo ya registrado")
                elif "INVALID_EMAIL" in error_registro:
                    mostrar_aviso(self.page, self.vista,"El correo electrónico no es válido")
                else:
                    mostrar_aviso(self.page, self.vista,"Error al registrar")

                # limpiamos los campos de la contraseña tras saltar un error
                self.vista.psw_input.value = ""
                self.vista.psw_confirmar.value = ""

        self.page.update()

    async def conectarse(self, e):
        mostrar_aviso(self.page, self.vista,"")
        self.page.update()

        if not self.vista.email_input.value or not self.vista.psw_input.value:
            mostrar_aviso(self.page, self.vista,"Introduce email y contraseña")
        else:
            conectado, aviso = await self.service.iniciar_sesion(self.vista.email_input.value,self.vista.psw_input.value)
            if conectado:
                self.page.update()               
                self.page.go("/home") # ruta a la pantalla principal/perfil/grupos
            else:
                error_log = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "INVALID_LOGIN_CREDENTIALS" in error_log or "INVALID_PASSWORD" in error_log:
                    mostrar_aviso(self.page, self.vista,"Email o contraseña incorrectos")
                elif "USER_NOT_FOUND" in error_log:
                    mostrar_aviso(self.page, self.vista,"Usuario no encontrado")
                elif "TOO_MANY_ATTEMPTS" in error_log:
                    mostrar_aviso(self.page, self.vista,"Demasiados intentos. Inténtalo más tarde")
                else:
                    mostrar_aviso(self.page, self.vista,"Error al conectarse")

                # limpiamos el campo de la contraseña y dejamos el focus ahí tras saltar un error    
                self.vista.psw_input.value = ""
                await self.vista.psw_input.focus()

        self.page.update()

    async def recuperar_psw(self, e):
        mostrar_aviso(self.page, self.vista,"")
        self.page.update()

        if not self.vista.email_input.value:
            mostrar_aviso(self.page, self.vista,"Introduce un email")
        else:
            enviado, aviso = await self.service.recu_psw(self.vista.email_input.value)
            if enviado:
                mostrar_aviso(self.page, self.vista,"Email de recuperación enviado. Revisa tu bandeja de entrada", color="#1A6AFE")
                self.page.update()
                await asyncio.sleep(1.5)    
                self.page.go("/")
            else:
                error_recu = str(aviso).upper() # convertimos el diccionario del aviso en texto en mayuscula para poder comprobar los errores
                if "NOT_FOUND" in error_recu:
                    mostrar_aviso(self.page, self.vista,"No existe ninguna cuenta asociada a este email")
                elif "INVALID_EMAIL" in error_recu:
                    mostrar_aviso(self.page, self.vista,"Formato de email incorrecto")
                else:
                    mostrar_aviso(self.page, self.vista,"Error al procesar la solicitud")

        self.page.update()