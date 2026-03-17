# archivo que recibe lo que se introduce por pantalla y le dice al wrapper que tiene que hacer

import flet as ft

class AuthController:
    # aquí recibimos el wrapper y lo guardamos para poder usarlo en toda la clase
    def __init__(self,page,wrapper):
        self.page = page
        self.wrapper = wrapper

    # parte de la lógica de 'LOGIN' y 'REGISTRO'
    async def conectarse(self,email,psw,mensaje):
        # comprobar que los campos de email y psw no están vacíos
        if not email.value or not psw.value:
            mensaje.value = "Tienes que rellenar todos los campos"
            self.page.update()
            return

        # usamos el wrapper para iniciar sesión
        conectado = await self.wrapper.inicio_sesion(email.value,psw.value)

        # si se ha podido iniciar sesion se abre el perfil del usuario
        if conectado:
            await self.page.push_route("/perfil")
        else:
            mensaje.value = "Correo o contraseña incorrectos"
            self.page.update() # se vuelve a mostrar la página de login

    async def registrarse(self,nombre,email,psw,telefono,mensaje):
        # comprobar que todos los campos se han rellenado (menos id_grupo que creamos vacío)
        datos = [nombre.value,email.value,psw.value,telefono.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
            self.page.update()
            return

        # comprobamos que la contraseña tenga un mínimo de 8 caracteres
        if len(psw.value)<8:
            mensaje.value = "La contraseña tiene que tener mínimo 8 caracteres"
            self.page.update()
            return

        # usamos el wrapper para registrar un usuario
        registrado = self.wrapper.registro(
            email = email.value,
            psw = psw.value,
            nombre = nombre.value,
            telefono = telefono.value
        )

        # si se ha registrado correctamente se abre el login
        if registrado:
            nombre.value = ""
            email.value = ""
            psw.value = ""
            telefono.value = ""
            mensaje.value = ""
            await self.page.push_route("/")
            self.page.update()
        else:
            mensaje.value = "Error al registrar el usuario"
            self.page.update()