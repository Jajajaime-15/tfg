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
                "id_grupo":"", # se rellena cuando se tenga una familia
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
            infor_usuario = self.db.child("usuarios").child(self.id_usuario).get(self.token).val() 
            if infor_usuario and "id_grupo" in infor_usuario: # comprobamos si en los datos del usuario ya tiene algun grupo asociado y se guarda en el dispositivo para poder recuperarlo
                grupo = infor_usuario["id_grupo"]
                await self.page.shared_preferences.set("id_grupo",grupo)
                print(f"Grupo:{grupo}")
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

    # función para registrar grupos nuevos
    async def crear_grupo(self, nombre_grupo):
    
        try:
            # Verifica que el usuario esté autenticado antes de crear un grupo
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para crear un grupo"
            
            # Los datos del grupo
            info_grupo = {
                "nombre": nombre_grupo,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Guarda el grupo en la base de datos
            grupos_ref = self.db.child("grupos")
            resultado = grupos_ref.push(info_grupo, self.token)  
            id_grupo = resultado["name"]  
            
            # Asigna el grupo al usuario que lo creó
            usuario_ref = self.db.child("usuarios").child(self.id_usuario)
            usuario_ref.update({
                "id_grupo": id_grupo
            }, self.token)
            
            print(f"Grupo '{nombre_grupo}' creado correctamente con ID: {id_grupo}")
            return True, "Grupo creado correctamente"
            
        except Exception as e:
            print(f"Error al crear grupo: {e}")
            return False, str(e)    

    # función para recuperar la contraseña mediante el correo
    async def recu_psw(self,email):
        try:
            self.auth.send_password_reset_email(email) # firebase envía automáticamente un correo al email que se indique (tiene que ser un email registrado)
            print("Correo enviado para recuperar contraseña")
            return True, "Correo enviado para recuperar tu contraseña"
        except Exception as e:
            print(f"Error al enviar el correo:{e}")
            return False, str(e)