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
        print(f"ID de usuario cargado: {self.id_usuario}")
        self.token = await self.page.shared_preferences.get("token")     

    # función para registrar grupos nuevos
    async def crear_grupo(self, nombre_grupo, integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para crear un grupo"
            
            info_grupo = {
                "admin": self.id_usuario,
                "nombre": nombre_grupo,
                "miembros": integrante,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Guardar en nodo "grupos"
            grupos_ref = self.db.child("grupos")
            resultado = grupos_ref.push(info_grupo, self.token)  
            id_grupo = resultado["name"]  
            
            # Obtener los grupos actuales del usuario
            ruta_completa = f"usuarios/{self.id_usuario}/id_grupo"
            grupos_actuales = self.db.child(ruta_completa).get(self.token).val()
            
            if grupos_actuales and isinstance(grupos_actuales, dict) and "grupos" in grupos_actuales:
                grupos_usuario = grupos_actuales["grupos"]
            else:
                grupos_usuario = {}
            
            print(f"Grupos actuales: {grupos_usuario}")
            
            # Añadir el nuevo grupo
            grupos_usuario[id_grupo] = nombre_grupo
            
            # Guardarlo actualizado en la base de datos
            self.db.child(ruta_completa).set({"grupos": grupos_usuario}, self.token)
            
            print(f"Grupo '{nombre_grupo}' creado correctamente con ID: {id_grupo}")
            return True, "Grupo creado correctamente"
            
        except Exception as e:
            print(f"Error al crear grupo: {e}")
            return False, str(e)

        
    # función para eliminar grupos
    async def eliminar_grupo(self, nombre_grupo):
        #FALTA CAMBIAR QUE SE ELIMINE TAMBIEN DEL USUARIO
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para eliminar un grupo"

            # Obtener todos los grupos
            todos_los_grupos = self.db.child("grupos").get(self.token).val()
            
            if not todos_los_grupos:
                return False, "No hay grupos en la base de datos"
            
            # Buscar el ID del grupo por nombre y verificar que sea admin
            id_grupo_encontrar = None
            for id_grupo, datos_grupo in todos_los_grupos.items():
                if datos_grupo.get("nombre") == nombre_grupo and datos_grupo.get("admin") == self.id_usuario:
                    id_grupo_encontrar = id_grupo
                    break
            
            if not id_grupo_encontrar:
                return False, f"No se encontró el grupo '{nombre_grupo}' o no eres el administrador"
            
            # Eliminar el grupo del nodo grupos
            self.db.child(f"grupos/{id_grupo_encontrar}").remove(self.token)
            
            # Eliminar el grupo del usuario
            ruta_usuario = f"usuarios/{self.id_usuario}/id_grupo/grupos"
            grupos_usuario = self.db.child(ruta_usuario).get(self.token).val()
            
            if grupos_usuario and id_grupo_encontrar in grupos_usuario:
                del grupos_usuario[id_grupo_encontrar]
                self.db.child(ruta_usuario).set(grupos_usuario, self.token)
            
            print(f"Grupo '{nombre_grupo}' eliminado correctamente")
            return True, "Grupo eliminado correctamente"
            
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)


    async def mostrar_grupos(self):
    
        nombres_grupos = []  
        integrantes = []

        try:
            if not self.token or not self.id_usuario:
                return [], "Debes iniciar sesión para ver los grupos", False  
            
            # Obtener todos los grupos
            grupos = self.db.child("grupos").get(self.token).val()

            
            if not grupos:
                print("No hay grupos en la base de datos")
                return [], "No hay grupos", True
            
            for datos_grupo in grupos.values():
                if datos_grupo.get("admin") == self.id_usuario:  # Solo los grupos donde el usuario es admin
                    nombres_grupos.append(datos_grupo.get("nombre", "Sin nombre"))
                    
                    # Obtener integrantes
                    miembros = datos_grupo.get("miembros", [])
                    if isinstance(miembros, str):
                        miembros = [miembros] if miembros else []
                    
                    integrantes.append(miembros)
            
            if not nombres_grupos:
                print("No eres admin de ningún grupo")
                return [], "No eres admin de ningún grupo", True
            
            return nombres_grupos, integrantes, True
            
        except Exception as e:
            print(f"Error al mostrar grupos: {e}")
            return [], [], False
        
    
    async def anyadir_participante(self, nombre_grupo, nuevo_integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para añadir participantes"
            
            # Obtener todos los grupos
            grupos = self.db.child("grupos").get(self.token).val()
            
            if not grupos:
                return False, "No hay grupos en la base de datos"
            
            # Buscar el grupo por nombre y admin 
            id_grupo_encontrar = None
            datos_grupo_encontrar = None
            
            for id_grupo, datos_grupo in grupos.items():
                if datos_grupo.get("nombre") == nombre_grupo and datos_grupo.get("admin") == self.id_usuario:
                    id_grupo_encontrar = id_grupo
                    datos_grupo_encontrar = datos_grupo
                    break
            
            if not id_grupo_encontrar:
                return False, f"No se encontró el grupo '{nombre_grupo}' o no eres el administrador"
            
            # Obtener los miembros
            miembros = datos_grupo_encontrar.get("miembros", [])
            
            # Verificar que miembros sea una lista
            if isinstance(miembros, str):
                miembros = [miembros] if miembros else []
            elif miembros is None:
                miembros = []
            
            # Verificar si ya existe
            if nuevo_integrante in miembros:
                return False, "El integrante ya está en el grupo"
            
            # Añadir el nuevo integrante
            miembros.append(nuevo_integrante)
            
            # Actualizar usando el ID del grupo
            self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token)
            
            print(f"Integrante '{nuevo_integrante}' añadido al grupo '{nombre_grupo}'")
            return True, "Integrante añadido correctamente"

        except Exception as e:
            print(f"Error al añadir participante: {e}")
            return False, str(e)
            
            