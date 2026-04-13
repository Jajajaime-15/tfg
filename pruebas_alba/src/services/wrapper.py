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
            refresh_token = usuario["refreshToken"]

            info_usuario = {
                "nombre": nombre,
                "telefono": telefono,
                "email": email,
                "pais": "", # se podrá rellenar desde el perfil de usuario
                "localidad": "", # ''
                "id_grupo":"", # se rellena cuando se tenga una familia
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
            refresh_token = usuario["refreshToken"]

            # obtenemos la infor del usuario de Realtime
            infor_usuario = self.db.child("usuarios").child(self.id_usuario).get(self.token).val() 

            # guardamos la infor en el dispositivo para que se puedan leer
            if infor_usuario:
                await self.page.shared_preferences.set("id_usuario", self.id_usuario)
                await self.page.shared_preferences.set("token", self.token)
                await self.page.shared_preferences.set("refresh_token", refresh_token)
                await self.page.shared_preferences.set("nombre", infor_usuario.get("nombre", ""))
                await self.page.shared_preferences.set("email", infor_usuario.get("email", ""))
                await self.page.shared_preferences.set("telefono", infor_usuario.get("telefono", ""))
                await self.page.shared_preferences.set("pais", infor_usuario.get("pais", ""))
                await self.page.shared_preferences.set("localidad", infor_usuario.get("localidad", ""))
                if "id_grupo" in infor_usuario:
                    await self.page.shared_preferences.set("id_grupo",infor_usuario["id_grupo"])
                
                print(f"Grupo:{infor_usuario.get("id_grupo")}")
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
                await self.page.shared_preferences.set("token",self.token)
                print("Token actualizado")
                return True
            return False
        except Exception as e:
            print(f"No se pudo actualizar la sesion:{e}")
            return False
        
    # funcion para actualizar los datos del usuario
    async def actualizar_datos(self,datos_actualizados):
        try:
            # recuperamos el id del usuario y el token
            if not self.id_usuario:
                self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            if not self.token:
                self.token = await self.page.shared_preferences.get("token")
            # intentamos actualizar los datos
            try:
                self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados, self.token)
            except Exception as e:
                print ("Token caducado")
                # llamamos a la funcion para actualizar el token
                if await self.actualizar_sesion():
                    try:
                        # volvemos a intentar actualizar los datos
                        self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados,self.token)
                    except Exception as x:
                        print("Error después de actualizar el token")
                        return False, f"Error después de actualizar el token{x}"
                else:
                    print ("Sesion caducada")
                    return False, "Sesion caducada, inicia sesión de nuevo"
            # guardamos los datos en el dispositivo
            for clave, valor in datos_actualizados.items():
                await self.page.shared_preferences.set(clave,valor)
            print ("Datos actualizados")
            return True, "Datos actualizados"
        except Exception as e:
            print(f"Error: {e}")
            return False, str(e)

    # funcion para cambiar la contraseña estando conectado    
    async def cambiar_psw(self,nueva_psw):
        try:
            self.token = await self.page.shared_preferences.get("token")
            # obtenemos el token si no está en memoria
            if not self.token:
                return False, "TOKEN_EXPIRED"            
            # actualizamos la contraseña
            self.auth.change_password(self.token,nueva_psw)
            print("Contraseña actualizada")
            return True, "Contraseña actualizada"
        except Exception as e:
            mensaje = str(e).upper()
            print(f"DEBUG: Error detectado en Firebase: {mensaje}")
            if "CREDENTIAL_TOO_OLD" in mensaje or "SENSITIVE_OPERATION" in mensaje:
                return False, "REQUIRES_RECENT_LOGIN" 
            # si el token está caducado, refrescamos el token
            if await self.actualizar_sesion():
                try:
                    self.token = await self.page.shared_preferences.get("token")
                    self.auth.change_password(self.token,nueva_psw)
                    return True, "Contraseña actualizada"
                except:
                    return False, "REQUIRES_RECENT_LOGIN"
            return False, "Error desconocido"
        
    # funcion para eliminar la cuenta y los datos de dicha cuenta
    async def borrar_cuenta(self):
        try:
            if not self.id_usuario:
                self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            if not self.token:
                self.token = await self.page.shared_preferences.get("token")

            # borramos toda la informacion de la base de datos (de Realtime)
            self.db.child("usuarios").child(self.id_usuario).remove(self.token)
            # borramos el usuario de Authentication
            self.auth.delete_user_account(self.token)
            # una vez eliminado cerramos sesión
            await self.cerrar_sesion()

            print("Cuenta eliminada")
            return True, "La cuenta ha sido eliminada"
        except Exception as e:
            print(f"Error al borrar la cuenta: {e}")
            return False, "Error al eliminar cuenta, inténtalo de nuevo iniciando sesión"

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

            # Leer el campo id_grupo del usuario
            ruta_id_grupo = f"usuarios/{self.id_usuario}/id_grupo"
            
            # Leer diccionario de grupos
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
                aviso = True  #No tiene grupos

            return nombres_grupos, integrantes, aviso
            
        except Exception as e:
            print(f"Error al mostrar grupos: {e}")
            return [], [], False  # En caso de error, éxito=False  
    
    async def anyadir_participante(self, nombre_grupo, nuevo_integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para añadir participantes"
            
            # Leer todos los grupos del usuario
            ruta_grupos_usuario = f"usuarios/{self.id_usuario}/id_grupo"
            grupos_usuario = self.db.child(ruta_grupos_usuario).get(self.token).val()
            
            if not grupos_usuario:
                return False, "No tienes grupos para añadir participantes"
            
            # Buscar el grupo por nombre y obtener su ID
            buscar_id_grupo = None
            for id_grupo, info_grupo in grupos_usuario.items():
                if info_grupo.get("nombre") == nombre_grupo:
                    buscar_id_grupo = id_grupo
                    break
            
            if not buscar_id_grupo:
                return False, f"No se encontró el grupo '{nombre_grupo}'"
            
            # Obtener el grupo del nodo "grupos" para ver los integrantes actuales
            ruta_grupo = f"grupos/{buscar_id_grupo}"
            datos_grupo = self.db.child(ruta_grupo).get(self.token).val()
            
            if not datos_grupo:
                return False, "El grupo no existe en la base de datos"
            
            # Obtener la lista actual de integrantes
            integrantes_actuales = datos_grupo.get("integrante", "")
            
            # convertir a lista si es un string vacío o solo un nombre
            if isinstance(integrantes_actuales, str):
                if integrantes_actuales:
                    lista_integrantes = [integrantes_actuales]
                else:
                    lista_integrantes = []
            else:
                lista_integrantes = integrantes_actuales if isinstance(integrantes_actuales, list) else []
            
            # Verificar si el nuevo integrante ya existe
            if nuevo_integrante in lista_integrantes:
                return False, f"El integrante '{nuevo_integrante}' ya esta en el grupo"
            
            # Agregar el nuevo integrante a la lista
            lista_integrantes.append(nuevo_integrante)
            
            # Guardar la lista actualizada en el nodo grupos
            self.db.child(ruta_grupo).update({"integrante": lista_integrantes}, self.token)
            
            # Actualizar la copia dentro del usuario
            grupos_usuario[buscar_id_grupo]["integrante"] = lista_integrantes
            self.db.child(ruta_grupos_usuario).set(grupos_usuario, self.token)
            
            print(f" Integrante '{nuevo_integrante}' añadido al grupo '{nombre_grupo}'")
            return True, f" Integrante añadido correctamente"
            
        except Exception as e:
            print(f" Error al añadir participante: {e}")
            return False, str(e)