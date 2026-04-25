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

    async def cargar_datos_usuario(self):
        self.id_usuario = await self.page.shared_preferences.get("id_usuario")
        self.token = await self.page.shared_preferences.get("token")     

    # función para registrar grupos nuevos
    async def crear_grupo(self, nombre_grupo, integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para crear un grupo"
            
            # Guarda el grupo en la base de datos
            grupos_ref = self.db.child("grupos")
            resultado = grupos_ref.push(info_grupo, self.token)  
            id_grupo = resultado["name"]  

            # Los datos del grupo
            info_grupo = {
                id_grupo: {
                    "admin": self.id_usuario,
                    "nombre": nombre_grupo,
                    "miembros" : integrante,
                    "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
            }
            
            

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
                "grupos": {
                    "nombre": nombre_grupo,
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
        grupos = None 
        grupo = None 
        aviso = False

        try:
            if not self.token or not self.id_usuario:
                return [], "Debes iniciar sesión para ver los grupos", False  
            
            print("funciona service grupos")
            
            grupos = self.db.child("usuarios").child(self.id_usuario).child("id_grupo").get(self.token).val()
            #datos_grupo = self.db.child("usuarios").child(self.id_usuario).child("id_grupo").get(self.token)

            if grupos is None or not grupos:
                print("No hay grupos asociados a este usuario")
                return [], "No tienes grupos", True
            
            for grupo_id in grupos.keys():
                grupo = self.db.child("grupos").child(grupo_id).get(self.token).val()
                print(f"Datos del grupo: {grupo}")

                if grupo:
                    # Agregar nombre del grupo
                    nombres_grupos.append(grupo.get("nombre", "Sin nombre"))
                    miembros_grupo = self.db.child("grupos").child(grupo_id).child("integrante").get(self.token).val()
                    print(f"Miembros del grupo: {miembros_grupo}")
                    integrantes.append(miembros_grupo if miembros_grupo else [])
     

            

                     


            return nombres_grupos, integrantes, True
            
        except Exception as e:
            print(f"Error al mostrar grupos: {e}")
            return [], [], False
        
    async def anyadir_participante(self, nombre_grupo, nuevo_integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para añadir participantes"
            
            
            # Leer todos los grupos del usuario con ruta absoluta
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
        
        