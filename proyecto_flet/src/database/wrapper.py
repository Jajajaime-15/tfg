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

            # Obtener los grupos del usuario
            ruta_usuario_grupos = f"usuarios/{self.id_usuario}/id_grupo"
            grupos_usuario = self.db.child(ruta_usuario_grupos).get(self.token).val()
            
            if not grupos_usuario:
                return False, "No tienes grupos para eliminar"
            
            # Buscar el ID del grupo por nombre
            id_grupo_encontrar = None
            for id_grupo, info_grupo in grupos_usuario.items():
                if info_grupo.get("nombre") == nombre_grupo:
                    id_grupo_encontrar = id_grupo
                    break
            
            if not id_grupo_encontrar:
                return False, f"No se encontró el grupo '{nombre_grupo}'"
            
            # Eliminar el grupo del nodo "grupos"
            self.db.child(f"grupos/{id_grupo_encontrar}").remove(self.token)
            
            # Eliminar el grupo del diccionario del usuario
            del grupos_usuario[id_grupo_encontrar]
            
            # Guardar el diccionario actualizado del usuario
            self.db.child(ruta_usuario_grupos).set(grupos_usuario, self.token)
            
            print(f" Grupo '{nombre_grupo}' eliminado correctamente")
            return True, "Grupo eliminado correctamente"
            
        except Exception as e:
            print(f" Error al eliminar grupo: {e}")
            return False, str(e)


    # TIENES QUE CAMBIAR ESTO A LO QUE DIJIMOS, Y CAMBIAR LOS METODOS SIGUIENTES PORQUE EN ANYADIR PARTICIPANTE ESTAS TENIENDO QUE ESCRIBIR MAS VECES DE LAS NECESARIAS
    # Y TAMBIEN HAY QUE SEPARAR ESTO EN OTRO SERVICE DISTINTO, NO TODO EN EL WRAPPER, QUIZAS LLAMARLO GROUP SERVICE
    async def mostrar_grupos(self):
        
        nombres_grupos = []  
        integrantes = []  
        try:
            if not self.token or not self.id_usuario:
                return [], "Debes iniciar sesión para ver los grupos", False  # ✅ 3 valores  # SI VAIS A HACER ESTO Y DECIR QUE NO AL MENOS OCULTADLO BIEN, ES MUY OBVIO CUANDO HAY COMENTARIOS DE IA
            
            # ESTO AQUI SERIA ALGO ASI: grupos = self.db.child("usuarios").child(self.id_usuario).child("grupos").get(self.token).val()
            # ASI TENDRAS LOS GRUPOS A LOS QUE PERTENECE EL USUARIO, POR EJEMPLO: {"Grupo_01" : true, "Grupo_02" : true} (el true es por rellenar el dict, aqui sigues las keys y ya)
            datos_grupo = self.db.child("usuarios").child(self.id_usuario).child("id_grupo").get(self.token)
            # LUEGO AQUI RECORRES ALGO COMO for grupo_id in grupos.keys():
            # grupo = self.db.child("grupos").child(grupo_id).get(self.token).val()
            # Y LUEGO SERIA RECORRER CON ESO DE GRUPOS QUE HAS SACADO PARA ENCONTRAR SUS MIEMBROS PORQUE TENEMOS UN APARTADO PARA ELLO:
            # for u in grupo["miembros"].keys(): (aqui tmb por keys porque lo tenemos como "usuario":true)
            # usuario = self.db.child("usuarios").child(u).get(self.token).val()
            # Y AQUI YA LO CONTINUAS, LA IDEA ESTA AHI PERO TENDRA SUS FALLOS COMO LO HE HECHO, ASIQ REVISALO BIEN
            # SE QUE SUENA TEDIOSO PERO LA IDEA ES: 
            # 1. SACAR TODOS LOS GRUPOS A LOS QUE PERTENECE EL USUARIO 
            # 2. SACAR CADA GRUPO INDIVIDUALMENTE PARA RECORRERLO
            # 3. DE CADA GRUPO SACAR TODOS SUS MIEMBROS Y GUARDARLOS
            # NO SE SI SERIA NECESARIO MOSTRAR LOS MIEMBROS EN LA PANTALLA DE HOME, PERO SI AL VER LA INFO DE LOS GRUPOS, ASI COMO APUNTE
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
        
