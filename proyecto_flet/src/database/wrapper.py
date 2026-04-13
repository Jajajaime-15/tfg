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

    # función para recuperar la contraseña mediante el correo
    async def recu_psw(self,email):
        try:
            self.auth.send_password_reset_email(email) # firebase envía automáticamente un correo al email que se indique (tiene que ser un email registrado)
            print("Correo enviado para recuperar contraseña")
            return True, "Correo enviado para recuperar tu contraseña"
        except Exception as e:
            print(f"Error al enviar el correo:{e}")
            return False, str(e)
        
    # función para registrar grupos nuevos (VERSIÓN CON RUTAS COMPLETAS)
    async def crear_grupo(self, nombre_grupo, integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para crear un grupo"
            
            # Los datos del grupo
            info_grupo = {
                "nombre": nombre_grupo,
                "integrante": integrante,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Guarda el grupo en la base de datos
            grupos_ref = self.db.child("grupos")
            resultado = grupos_ref.push(info_grupo, self.token)  
            id_grupo = resultado["name"]  

            # RUTA COMPLETA para leer el campo id_grupo del usuario
            ruta_id_grupo = f"usuarios/{self.id_usuario}/id_grupo"
            
            # Leer diccionario de grupos usando ruta completa
            valor_actual = self.db.child(ruta_id_grupo).get(self.token).val()
            
            # Si es None o string, lo convertimos a diccionario vacío
            if not isinstance(valor_actual, dict):
                dic_grupos = {}
            else:
                dic_grupos = valor_actual

            print(f"Diccionario de grupos antes de añadir el nuevo grupo: {dic_grupos}")

            # Añadir el nuevo grupo al diccionario
            dic_grupos = {
                id_grupo: {
                    "nombre": nombre_grupo,
                    "integrante": integrante
                    }
            }
            
            # Guardar usando la misma RUTA COMPLETA
            print(f"Actualizando el usuario con el nuevo grupo: {dic_grupos}")
            self.db.child(ruta_id_grupo).update(dic_grupos, self.token)
            
            print(f"Grupo '{nombre_grupo}' creado correctamente con ID: {id_grupo}")
            return True, "Grupo creado correctamente"
            
        except Exception as e:
            print(f"Error al crear grupo: {e}")
            return False, str(e)

        
    # función para eliminar grupos
    async def eliminar_grupo(self, nombre_grupo):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para eliminar un grupo"

            datos_grupo = self.db.child("grupos").get(self.token)
            for grupo in datos_grupo.each():
                if grupo.val().get("nombre") == nombre_grupo:
                    id_grupo = grupo.key()
                    grupo_ref = self.db.child("grupos").child(id_grupo)
                    grupo_ref.remove(self.token)
                    print(f"Grupo '{nombre_grupo}' eliminado correctamente")
                    return True, "Grupo eliminado correctamente"
            
            return False, "No se ha encontrado el grupo que quieres eliminar"
            
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)


    
    async def mostrar_grupos(self):
        nombres_grupos = []  
        integrantes = []  
        try:
            if not self.token or not self.id_usuario:
                return [], "Debes iniciar sesión para ver los grupos", False  # ✅ 3 valores
            
            datos_grupo = self.db.child("usuarios").child(self.id_usuario).child("id_grupo").get(self.token)
            
            if datos_grupo.val() is not None:
                print("Hay grupos asociados a este usuario")
                nombres_grupos = [grupo.val().get("nombre") for grupo in datos_grupo.each()]
                integrantes = [grupo.val().get("integrante") for grupo in datos_grupo.each()]
                aviso = True
            else:
                print("No hay grupos asociados a este usuario")
                aviso = True  # No es error, solo no tiene grupos

            return nombres_grupos, integrantes, aviso
            
        except Exception as e:
            print(f"Error al mostrar grupos: {e}")
            return [], [], False  # En caso de error, éxito=False
                

    #async def anyadir_participante(self):

         
