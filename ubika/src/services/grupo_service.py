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
            print("Conectado a firebase")
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
            
            usuarios = self.db.child("usuarios").get(self.token).val()

            id_nuevo_integrante = None

            for id_usuario, datos_usuario in usuarios.items():
                if datos_usuario.get("email") == integrante:
                    id_nuevo_integrante = id_usuario
                    print(f"Nuevo integrante encontrado: {id_nuevo_integrante} (ID de usuario)")
                    break

            if not id_nuevo_integrante:
                print("No se encontró el usuario con email:", integrante)
                return False, f"No se encontró el usuario con email {integrante}"    
            
            miembros = {
                self.id_usuario: True,
                id_nuevo_integrante: True}
            
            info_grupo = {
                "admin": self.id_usuario,
                "nombre": nombre_grupo,
                "miembros": miembros,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Guardar en nodo "grupos"
            grupos_ref = self.db.child("grupos")
            resultado = grupos_ref.push(info_grupo, self.token)  
            id_grupo = resultado["name"]  
            
            # Obtener los grupos actuales del usuario
            ruta_completa = f"usuarios/{self.id_usuario}/grupos"
            grupos_actuales = self.db.child(ruta_completa).get(self.token).val()
            
            ruta_admin = f"usuarios/{self.id_usuario}/grupos"
            grupos_admin = self.db.child(ruta_admin).get(self.token).val()
            
            # Si no hay grupos o no es diccionario lo creamos como un diccionario vacío
            if not grupos_admin or not isinstance(grupos_admin, dict):
                grupos_admin = {}
            
            # Añadir el nuevo grupo sin borrar los anteriores
            grupos_admin[id_grupo] = True
            
            self.db.child(ruta_admin).update(grupos_admin, self.token)
            
            # Actualizar los grupos del nuevo integrante
            ruta_integrante = f"usuarios/{id_nuevo_integrante}/grupos"
            grupos_integrante = self.db.child(ruta_integrante).get(self.token).val()
            
            if not grupos_integrante or not isinstance(grupos_integrante, dict):
                grupos_integrante = {}
            
            grupos_integrante[id_grupo] = True
            self.db.child(ruta_integrante).update(grupos_integrante, self.token)
            
            print(f"Grupo '{nombre_grupo}' creado correctamente con ID: {id_grupo}")
            return True, "Grupo creado correctamente"
            
        except Exception as e:
            print(f"Error al crear grupo: {e}")
            return False, str(e)

        
    async def eliminar_grupo(self, nombre_grupo):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para eliminar un grupo"

            # Obtener todos los grupos
            todos_los_grupos = self.db.child("grupos").get(self.token).val()
            
            if not todos_los_grupos:
                return False, "No hay grupos en la base de datos"
            
            # Buscar el grupo
            id_grupo_encontrar = None
            datos_grupo_encontrar = None
            
            for id_grupo, datos_grupo in todos_los_grupos.items():
                if datos_grupo.get("nombre") == nombre_grupo and datos_grupo.get("admin") == self.id_usuario:
                    id_grupo_encontrar = id_grupo
                    datos_grupo_encontrar = datos_grupo
                    break
            
            if not id_grupo_encontrar:
                return False, f"No se encontró el grupo '{nombre_grupo}' o no eres el administrador"
            
            # Obtener la lista de miembros
            miembros = datos_grupo_encontrar.get("miembros", {})
            
            # Eliminar el grupo de todos los miembros
            for id_miembro in miembros.keys():
                # Ruta completa al grupo específico del usuario
                ruta_grupo_usuario = f"usuarios/{id_miembro}/grupos/{id_grupo_encontrar}"
                
                # Verificar si existe la referencia
                grupo_ref = self.db.child(ruta_grupo_usuario).get(self.token).val()
                if grupo_ref:
                    # Eliminar la referencia del grupo de este usuario
                    self.db.child(ruta_grupo_usuario).remove(self.token)
                    print(f"  ✓ Referencia eliminada para usuario: {id_miembro}")
            
            # Eliminar el grupo del nodo principal
            self.db.child(f"grupos/{id_grupo_encontrar}").remove(self.token)
            
            print(f"Grupo '{nombre_grupo}' eliminado completamente")
            
            return True, "Grupo eliminado correctamente"
            
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)

    # función para editar grupos
    async def editar_grupo(self, nombre_grupo, nuevo_nombre_grupo):
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
            
            # Editar el nombre del grupo
            self.db.child(f"grupos/{id_grupo_encontrar}").update({"nombre": nuevo_nombre_grupo}, self.token)
            
            # Editar el nombre del grupo del usuario
            ruta_usuario = f"usuarios/{self.id_usuario}/grupos"
            grupos_usuario = self.db.child(ruta_usuario).get(self.token).val()
            

            # Verificar que grupos_usuario es un diccionario y contiene el grupo
            if grupos_usuario and isinstance(grupos_usuario, dict) and id_grupo_encontrar in grupos_usuario:
                # Actualizar el nombre del grupo en el diccionario del usuario
                grupos_usuario[id_grupo_encontrar] = nuevo_nombre_grupo
                # Guardar el diccionario actualizado
                self.db.child(ruta_usuario).set(grupos_usuario, self.token)
            
            print(f"Grupo '{nombre_grupo}' editado correctamente")
            return True, "Grupo editado correctamente"
            
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)    


    async def mostrar_grupos(self):
    
        nombres_grupos = []  
        integrantes_con_nombres = [] 

        try:
            if not self.token or not self.id_usuario:
                return [], "Debes iniciar sesión para ver los grupos", False  
            
            # Obtener todos los grupos y usuarios
            grupos = self.db.child("grupos").get(self.token).val()
            usuarios = self.db.child("usuarios").get(self.token).val()
            
            if not grupos:
                print("No hay grupos en la base de datos")
                return [], "No hay grupos", True
            
            # Recorrer todos los grupos
            for clave_grupo, datos_grupo in grupos.items():
                grupos_usuario = datos_grupo.get("miembros", {})
                
                # Si es un string, convertirlo a diccionario vacío
                if isinstance(grupos_usuario, str):
                    grupos_usuario = {}
                elif grupos_usuario is None:
                    grupos_usuario = {}
                
                # Verificar si el usuario esta en los miembros
                if isinstance(grupos_usuario, dict) and self.id_usuario in grupos_usuario:
                    nombres_grupos.append(datos_grupo.get("nombre", "Sin nombre"))
                    print(f"Usuario {self.id_usuario}")
                    print(f"Grupos: {nombres_grupos}")
                    
                    # Obtener integrantes
                    nombres_integrantes = []
                    
                    # Verificar que miembros es un diccionario
                    if isinstance(grupos_usuario, dict):
                        for id_integrante in grupos_usuario.keys():
                            # Buscar el nombre del usuario por su ID
                            if usuarios and id_integrante in usuarios:
                                nombre_usuario = usuarios[id_integrante].get("nombre", id_integrante)
                                nombres_integrantes.append(nombre_usuario)
                            else:
                                nombres_integrantes.append(f"Desconocido ({id_integrante})")
                    
                    integrantes_con_nombres.append(nombres_integrantes)
            
            if not nombres_grupos:
                print(f"No eres miembro de ningún grupo. Tu ID: {self.id_usuario}")
                return [], f"No eres miembro de ningún grupo (ID: {self.id_usuario})", True
            
            return nombres_grupos, integrantes_con_nombres, True
            
        except Exception as e:
            print(f"Error al mostrar grupos: {e}")
            return [], [], False
            
        
    
    async def anyadir_participante(self, nombre_grupo, nuevo_integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para añadir participantes"
            
            # Obtener todos los grupos
            grupos = self.db.child("grupos").get(self.token).val()
            usuarios = self.db.child("usuarios").get(self.token).val()

            
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
            miembros = datos_grupo_encontrar.get("miembros", {})
            
            # Verificar que miembros sea un diccionario
            if not isinstance(miembros, dict):
                miembros = {}

            id_integrante = None

            for id_usuario, datos_usuario in usuarios.items():
                if datos_usuario.get("email") == nuevo_integrante:
                    id_integrante = id_usuario
                    datos_usuario_encontrar = datos_usuario
                    print(f"Nuevo integrante encontrado: {id_integrante} (ID de usuario)")
                    break    

            grupos_integrante = datos_usuario_encontrar.get("grupos", {})    

            # Verificar que grupos_integrante sea un diccionario
            if not isinstance(grupos_integrante, dict):
                grupos_integrante = {}
            
            grupos_integrante[id_grupo_encontrar] = True
    
            # Verificar que miembros sea un diccionario
            if not isinstance(miembros, dict):
                miembros = {}
            
            if not id_integrante:
                print("No se encontró el usuario con email:", nuevo_integrante)
                return False, f"No se encontró el usuario con email {nuevo_integrante}"

            # Verificar si ya existe
            if id_integrante in miembros:
                return False, "El integrante ya está en el grupo"
            
            # Añadir el nuevo integrante
            miembros[id_integrante] = True
            
            # Actualizar usando el ID del grupo
            self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token)
            self.db.child(f"usuarios/{id_integrante}/grupos").update(grupos_integrante, self.token)
            
            print(f"Integrante '{nuevo_integrante}' añadido al grupo '{nombre_grupo}'")
            return True, "Integrante añadido correctamente"

        except Exception as e:
            print(f"Error al añadir participante: {e}")
            return False, str(e)
        
    async def eliminar_participante(self, nombre_grupo, nombre_integrante):
        try:
            if not self.token or not self.id_usuario:
                return False, "Debes iniciar sesión para eliminar participantes"
            
            # Obtener todos los grupos
            grupos = self.db.child("grupos").get(self.token).val()
            
            if not grupos:
                return False, "No hay grupos en la base de datos"
            
            # Buscar el grupo por nombre
            id_grupo_encontrar = None
            datos_grupo_encontrar = None
            
            for id_grupo, datos_grupo in grupos.items():
                if datos_grupo.get("nombre") == nombre_grupo:
                    id_grupo_encontrar = id_grupo
                    datos_grupo_encontrar = datos_grupo
                    break
            
            if not id_grupo_encontrar:
                return False, f"No se encontró el grupo '{nombre_grupo}'"
            
            # Verificar que sea admin
            if datos_grupo_encontrar.get("admin") != self.id_usuario:
                return False, "Solo el administrador puede eliminar participantes"
            
            # Obtener miembros
            miembros = datos_grupo_encontrar.get("miembros", {})
            
            if not isinstance(miembros, dict):
                miembros = {}
            
            # Buscar el ID del integrante por nombre
            usuarios = self.db.child("usuarios").get(self.token).val()
            id_integrante_eliminar = None
            
            for id_usuario, datos_usuario in usuarios.items():
                if datos_usuario.get("nombre") == nombre_integrante:
                    id_integrante_eliminar = id_usuario
                    break
            
            if not id_integrante_eliminar:
                return False, f"No se encontró el integrante '{nombre_integrante}'"
            
            # No permitir eliminar al admin
            if id_integrante_eliminar == self.id_usuario:
                return False, "No puedes eliminarte a ti mismo del grupo"
            
            # Eliminar del diccionario de miembros
            if id_integrante_eliminar in miembros:
                del miembros[id_integrante_eliminar]
                
                # Actualizar en Firebase
                self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token)
                
                # Eliminar referencia del grupo en el usuario eliminado
                ruta_usuario = f"usuarios/{id_integrante_eliminar}/grupos/{id_grupo_encontrar}"
                self.db.child(ruta_usuario).remove(self.token)
                
                print(f"Integrante '{nombre_integrante}' eliminado del grupo '{nombre_grupo}'")
                return True, "Integrante eliminado correctamente"
            else:
                return False, "El integrante no está en el grupo"
                
        except Exception as e:
            print(f"Error al eliminar participante: {e}")
            return False, str(e)    