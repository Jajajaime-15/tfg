<<<<<<< HEAD
import json

class UsuarioService:
    def __init__(self, page, firebase_service, auth_service):
            self.page = page
            self.fb = firebase_service
            self.auth_s = auth_service
            self.db = firebase_service.db
            self.id_usuario = None
            self.token = None

    # funcion para actualizar los datos del usuario
    async def actualizar_datos(self, datos_actualizados):
        try:
            self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            # cogemos el token del auth_service
            token_actual = await self.auth_s.coger_token()

            try:
                self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados, token_actual)
            except Exception as e:
                error_str = str(e).upper()
                if "ID_TOKEN" in error_str or "EXPIRED" in error_str or "INVALID" in error_str:
                    print("Token caducado.")
                    if await self.auth_s.actualizar_sesion(): # llamamos a la funcion para actualizar el token
                        # volvemos a intentarlo con el token nuevo
                        token_nuevo = await self.auth_s.coger_token()
                        self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados, token_nuevo)
                        print("Datos actualizados.")
                    else:
                        print("Sesion expirada, vuelve a iniciar sesión")
                        return False, "SESION_EXPIRADA"
                else:
                    print("Error en firebase")
                    raise e
                
            # guardamos los datos en el dispositivo    
            for clave, valor in datos_actualizados.items():
                val_str = str(valor).lower() if isinstance(valor, bool) else str(valor) # convertimos todo a str porque shared preferences no adminte booleanos ni diccionarios
                await self.page.shared_preferences.set(clave, val_str)
                print("Datos actualizados en el dispositivo")
            return True, "Datos actualizados"
        except Exception as e:
            print(f"Error al actualizar: {e}")
            return False, str(e)
        
    # funcion para que se sincronice con los datos que hay firebase 
    async def sincronizar (self):
        try:
            self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            self.token = await self.page.shared_preferences.get("token")

            if self.id_usuario and self.token:
                try:
                    infor = self.db.child("usuarios").child(self.id_usuario).get(self.token).val()   
                except Exception as e:
                    error_str = str(e).upper()
                    if "401" in error_str or "PERMISSION DENIED" in error_str:
                        print("Intentando refrescar token...")
                        if await self.auth_s.actualizar_sesion():
                            self.token = await self.page.shared_preferences.get("token")
                            # Segundo intento con el nuevo token
                            infor = self.db.child("usuarios").child(self.id_usuario).get(self.token).val()
                        else:
                            print("No se pudo recuperar la sesión activa.")
                            return
                if infor:
                    # diccionario de las cosas que queremos guardar en el dispositivo
                    datos_a_guardar = {
                        "nombre": infor.get("nombre", ""),
                        "apellidos": infor.get("apellidos", ""),
                        "email": infor.get("email", ""),
                        "telefono": infor.get("telefono", ""),
                        "pais": infor.get("pais", ""),
                        "localidad": infor.get("localidad", ""),
                        "color_avatar": infor.get("color_avatar", "#1A6AFE"),
                        "compartir_ubicacion": infor.get("compartir_ubicacion", "false")
                    }

                    # sincronizamos los grupos en el caso de que tenga
                    if "grupos" in infor:
                        datos_a_guardar["grupos"] = json.dumps(infor.get("grupos", {}))
                        
                    # guardamos todo a la vez
                    for clave, valor in datos_a_guardar.items():
                        await self.page.shared_preferences.set(clave, str(valor))
                    print("Sincronizado con firebase")
                else:
                    for datos in ["nombre", "apellidos", "email", "telefono", "pais", "localidad"]:
                        await self.page.shared_preferences.remove(datos)
                    print("No hay informacion de este usuario en la base de datos")
            else:
                print("No hay una sesion activa")
        except Exception as e:
            print(f"Error al sincronizar: {e}")
=======
# inicializar Firebase + funciones necesarias

import pyrebase
from database.config import config
from datetime import datetime

class Wrapper:
    def __init__(self,page):
        self.page = page
        try:
            self.firebase = pyrebase.initialize_app(config)
            self.auth = self.firebase.auth()
            self.db = self.firebase.database()
            self.id_usuario = None
            self.id_grupo = None
            self.token = None
            print("Conectado a firebase") # print para comprobar que no hay problema a la hora de conectarse
        except Exception as e:
            print("Error al conectarse a firebase")

    # función para registrar usuarios nuevos
    async def registrarse (self, nombre, telefono, email, psw):
        try:
            usuario = self.auth.create_user_with_email_and_password(email,psw)
            self.id_usuario = usuario["localId"]
            self.token = usuario["idToken"]
            info_usuario = {
                "nombre": nombre,
                "telefono": telefono,
                "email": email,
                "grupos":"", # se rellena cuando se tenga una familia
                "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # se usa strtime porque firebase no lee fechas, tiene que ser texto o numeros
            }
            self.db.child("usuarios").child(self.id_usuario).set(info_usuario,self.token) # guardamos la informacion del usuario y el token en la base de datos
            print("Usuario registrado correctamente")
            return True,"Usuario registrado correctamente"
        except Exception as e:
            print(f"Error a la hora de registrar: {e}")
            return False, str(e)

    # función para iniciar sesión con un usuario ya registrado
    async def iniciar_sesion (self,email,psw):
        try:
            usuario = self.auth.sign_in_with_email_and_password(email, psw)
            self.id_usuario = usuario["localId"]
            self.token = usuario["idToken"]
            await self.page.shared_preferences.set("id_usuario", self.id_usuario) # guardamos el id del usuario en el dispositivo
            await self.page.shared_preferences.set("token", self.token)  # guardamos el token en el dispositivo para poder usarlo en otras funciones sin tener que pedir al usuario que inicie sesión cada vez
            
            print("Sesión iniciada")
            return True, "Sesión iniciada correctamente"
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False, str(e)
    
    # funcion para no pedir iniciar sesion cada vez que se abra la aplicacion
    async def usuario_conectado(self):
        try:
            return await self.page.shared_preferences.get("id_usuario")
        except:
            print("Error al recuperar usuario")
            return None
    
    # función para cerrar la sesión de un usuario
    async def cerrar_sesion(self):
        try:
            await self.page.shared_preferences.clear() # borramos toda la información que hay guardada en el dispositivo
            self.id_usuario = None
            self.token = None
            self.page.go("/") # .push_route("/") redirige al inicio (login) ((ANTES ERA .GO))
            print("Sesión cerrada")
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")

    # función para recuperar la contraseña mediante el correo
    async def recu_psw(self,email):
        try:
            self.auth.send_password_reset_email(email) # firebase envía automáticamente un correo al email que se indique (tiene que ser un email registrado)
            print("Correo enviado para recuperar contraseña")
            return True, "Correo enviado para recuperar tu contraseña"
        except Exception as e:
            print(f"Error al enviar el correo:{e}")
            return False, str(e)
        
    
>>>>>>> 3c1733a84dbc055c42901ba1860dccc64ccd6358
