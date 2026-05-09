from datetime import datetime
import json

class AuthService:
    def __init__(self, page, firebase_service):
        self.page = page
        self.fb = firebase_service
        self.auth = firebase_service.auth 
        self.db = firebase_service.db
        self.id_usuario = None
        self.token = None

    # función para registrar usuarios nuevos
    async def registrarse (self, nombre, telefono, email, psw):
        try:
            usuario = self.auth.create_user_with_email_and_password(email,psw)
            self.id_usuario = usuario["localId"]
            self.token = usuario["idToken"]
            refresh_token = usuario["refreshToken"]

            info_usuario = {
                "nombre": nombre,
                "telefono": telefono,
                "email": email,
                "pais": "", # se podrá rellenar desde el perfil de usuario
                "localidad": "", # ''
                "color_avatar": "#1A6AFE",
                "compartir_ubicacion": "false",
                "grupos":{}, # se rellena cuando se tenga una familia # REVISAR ESTO POR LA FORMA EN LA QUE GUARDAMOS LOS GRUPOS, DE LA FORMA ACTUAL SOLO SE PODRIA GUARDAR UNO
                "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # se usa strtime porque firebase no lee fechas, tiene que ser texto o numeros
            }
            self.db.child("usuarios").child(self.id_usuario).set(info_usuario,self.token) # guardamos la informacion del usuario y el token en la base de datos

            # guardamos los datos en el dispositivo para que al arrancar ya estén si inicia sesión con esa cuenta
            await self.page.shared_preferences.set("id_usuario", self.id_usuario)
            await self.page.shared_preferences.set("token", self.token)
            await self.page.shared_preferences.set("refresh_token", refresh_token)
            await self.page.shared_preferences.set("nombre", nombre)
            await self.page.shared_preferences.set("telefono", telefono)
            await self.page.shared_preferences.set("email", email)
            await self.page.shared_preferences.set("color_avatar", "#1A6AFE")
            await self.page.shared_preferences.set("compartir_ubicacion", "false")

            print("Usuario registrado correctamente")
            return True,"Usuario registrado correctamente"
        except Exception as e:
            print(f"Error a la hora de registrar: {e}")
            return False, str(e)

    # función para iniciar sesión con un usuario ya registrado
    async def iniciar_sesion (self, email, psw):
        try:
            usuario = self.auth.sign_in_with_email_and_password(email, psw)
            self.id_usuario = usuario["localId"]
            self.token = usuario["idToken"]
            refresh_token = usuario["refreshToken"]

            # se guarda lo que se necesita para arrancar la aplicacion y sincronizar 
            # (el resto se sincroniza al entrar en home con la funcion sincronizar)
            await self.page.shared_preferences.set("id_usuario", self.id_usuario)
            await self.page.shared_preferences.set("token", self.token)
            await self.page.shared_preferences.set("refresh_token", refresh_token)

            print("Sesión iniciada")
            return True, "Sesión iniciada correctamente"
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False, str(e)
    
    # funcion para no pedir iniciar sesion cada vez que se abra la aplicacion
    async def usuario_conectado(self):
        try:
            self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            self.token = await self.page.shared_preferences.get("token")
            # comprobamos que el id de usuario es None o una cadena vacía
            if not self.id_usuario or str(self.id_usuario).strip() in ["", "None", "null"]: 
                    return None
            return self.id_usuario
        except:
            print("Error al recuperar usuario")
            return None
    
    # función para cerrar la sesión de un usuario
    async def cerrar_sesion(self):
        try:
            datos_usuario = [
                "id_usuario", "token", "refresh_token", "nombre", 
                "apellidos", "email", "telefono", "pais", 
                "localidad", "grupos","color_avatar","compartir_ubicacion"
            ]

            # borramos los datos de la sesión pero el tema se mantiene
            for dato in datos_usuario:
                await self.page.shared_preferences.remove(dato)

            self.id_usuario = None
            self.token = None
            self.page.index_navegacion = 0 # al cerrar sesión y volver a iniciar arranca desde grupos
            print("Sesión cerrada")
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")

    # función para recuperar la contraseña mediante el correo
    async def recu_psw(self, email):
        try:
            self.auth.send_password_reset_email(email) # firebase envía automáticamente un correo al email que se indique (tiene que ser un email registrado)
            print("Correo enviado para recuperar contraseña")
            return True, "Correo enviado para recuperar tu contraseña"
        except Exception as e:
            print(f"Error al enviar el correo:{e}")
            return False, str(e)
    
    # funcion para que los servicios cojan el token actual
    async def coger_token(self):
        # cogemos el guardado en el dispositivo porque es el último/actual
        self.token = await self.page.shared_preferences.get("token")
        return self.token
    
    # funcion de actualizar sesion pidiendo a Firebase un nuevo Token
    async def actualizar_sesion(self):
        try:
            # recuperamos el refresh_token del dispositivo
            token_refresh = await self.page.shared_preferences.get("refresh_token")
            # pedimos a firebase el token nuevo
            if token_refresh:
                nuevo = self.auth.refresh(token_refresh)
                # actualizamos el token
                self.token = nuevo["idToken"]
                await self.page.shared_preferences.set("token",self.token) # guardamos el nuevo token
                if "refreshToken" in nuevo: # y si el refresh_token ha cambiado tambien lo guardamos
                    await self.page.shared_preferences.set("refresh_token",nuevo["refreshToken"])
                return True
            return False
        except Exception as e:
            print(f"No se pudo actualizar la sesion:{e}")
            return False
        