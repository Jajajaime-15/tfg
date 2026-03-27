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
    def registrarse (self, nombre, telefono, email, psw):
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
            self.db.child("usuarios").child(self.id_usuario).set(info_usuario,self.token)
            print("Usuario registrado correctamente")
            return True
        except Exception as e:
            print(f"Error a la hora de registrar: {e}")
            return False

    # función para iniciar sesión con un usuario ya registrado
    async def iniciar_sesion (self,email,psw):
        try:
            usuario = self.auth.sign_in_with_email_and_password(email,psw)
            self.id_usuario = usuario["localId"]
            self.token = usuario["idToken"]
            await self.page.shared_preferences.set("id_usuario", usuario["localId"]) # se guarda el id en el almacenamiento local(TOKEN)
            print("Sesión iniciada")
            return True
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False
    
    # funcion para no pedir iniciar sesion cada vez que se abra la aplicacion
    async def usuario_conectado(self):
        try:
            return await self.page.shared_preferences.get("id_usuario")
        except:
            return None
    
    # función para cerrar la sesión de un usuario
    async def cerrar_sesion(self):
        try:
            await self.page.shared_preferences.remove("id_usuario") # eliminar el usuario del almacenamiento local
            await self.page.push_route("/") # .push_route("/") redirige al inicio (login) ((ANTES ERA .GO))
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")

    # función para registrar usuarios nuevos
    def crear_grupo (self, nombre):
        try:
            currentUser = self.auth().current_user
            if not currentUser: # si no hay un usuario conectado, no se puede crear un grupo
                print("No hay un usuario conectado")
                return False
            else:
                id_usuario = currentUser["localId"]
                token = currentUser["idToken"]
                grupo = self.db.child("grupos").push({"nombre": nombre}, token) # se crea el grupo en la base de datos
                id_grupo = grupo["name"] # se obtiene el id del grupo creado
                self.db.child("usuarios").child(id_usuario).update({"id_grupo": id_grupo}, token) # se actualiza el usuario con el id del grupo al que pertenece
                print("Grupo creado correctamente")
            return True
        except Exception as e:
            print(f"Error a la hora de crear el grupo: {e}")
            return False        