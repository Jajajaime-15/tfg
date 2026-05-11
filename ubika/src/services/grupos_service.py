from datetime import datetime
import json

class GruposService:
    def __init__(self, page, firebase_service):
        self.page = page
        self.firebase = firebase_service # instanciamos firebase, su bbdd y la autenticacion
        self.auth = self.firebase.auth
        self.db = self.firebase.db
        self.id_usuario = None
        self.token = None
        self.todos_los_grupos_usuarios = None
        self.todos_los_usuarios = None

    async def buscar_grupos(self):
        try:
            todos_los_grupos = self.db.child("grupos").get(self.token).val() # Obtener todos los grupos
            if todos_los_grupos:
                return todos_los_grupos
            else:
                print(f"No se encontraron grupos")
                return []
        except Exception as e:
            print(f"Error al buscar grupos del usuario: {e}")
            return []
        
    async def grupos_del_usuario_admin(self, nombre_grupo):
        try:
            id_grupo_encontrar = None
            datos_grupo_encontrar = None
            todos_los_grupos = await self.buscar_grupos()
            for id_grupo, datos_grupo in todos_los_grupos.items():
                if datos_grupo.get("nombre") == nombre_grupo and datos_grupo.get("admin") == self.id_usuario:
                    id_grupo_encontrar = id_grupo
                    datos_grupo_encontrar = datos_grupo
                    return id_grupo_encontrar, datos_grupo_encontrar
            return False, f"No se encontró el grupo '{nombre_grupo}' o no eres el administrador"
        except Exception as e:
            print(f"Error al buscar grupos del usuario en grupos: {e}")
            return False, str(e)

    async def cargar_datos_usuario(self):
        self.id_usuario = await self.page.shared_preferences.get("id_usuario")
        self.token = await self.page.shared_preferences.get("token")

        if self.id_usuario and self.token:
            try:
                self.todos_los_grupos_usuarios = self.db.child("usuarios").child(self.id_usuario).child("grupos").get(self.token).val()
                self.todos_los_usuarios = self.db.child("usuarios").get(self.token).val()
                await self.actualizar_grupos_preferences()
            except Exception as e:
                print(f"Error al cargar datos del usuario: {e}")
        else:
            print("No se pudo cargar el ID de usuario o el token")    

    async def actualizar_grupos_preferences(self):
        try:
            if self.todos_los_grupos_usuarios is None:
                grupos_actualizados = {}
            else:
                grupos_actualizados = self.todos_los_grupos_usuarios
            
            await self.page.shared_preferences.set("grupos", json.dumps(grupos_actualizados))
        except Exception as e:
            print(f"Error al sincronizar grupos: {e}")        

    async def crear_grupo(self, nombre_grupo, integrante):
        try:
            await self.cargar_datos_usuario()  # Cargar datos del usuario
            
            id_nuevo_integrante = None

            for id_usuario, datos_usuario in self.todos_los_usuarios.items():
                if datos_usuario.get("email") == integrante:
                    id_nuevo_integrante = id_usuario
                    break

            if not id_nuevo_integrante:
                return False, f"No se encontró el usuario con email {integrante}"    
            
            miembros = {
                self.id_usuario: True,
                id_nuevo_integrante: True
            }
            
            info_grupo = {
                "admin": self.id_usuario,
                "nombre": nombre_grupo,
                "miembros": miembros,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            resultado = self.db.child("grupos").push(info_grupo, self.token) # Guardar en nodo "grupos"
            id_grupo = resultado["name"]  
            
            ruta_admin = f"usuarios/{self.id_usuario}/grupos"
            grupos_admin = await self.page.shared_preferences.get("grupos")

            if grupos_admin is None:
                print("No hay grupos guardados en shared_preferences")
                return [], [], [], False
            
            # Si es string pasar a JSON
            if isinstance(grupos_admin, str):
                try:
                    grupos_admin = json.loads(grupos_admin)
                except:
                    grupos_admin = {}
            
            if not grupos_admin or not isinstance(grupos_admin, dict): # Si no hay grupos o no es diccionario lo creamos como un diccionario vacío
                grupos_admin = {}

                
            
            grupos_admin[id_grupo] = True # Añadir el nuevo grupo sin borrar los anteriores
            self.db.child(ruta_admin).update(grupos_admin, self.token)

            await self.page.shared_preferences.set("grupos", json.dumps(grupos_admin))
            
            # Actualizar los grupos del nuevo integrante
            ruta_integrante = f"usuarios/{id_nuevo_integrante}/grupos"
            grupos_integrante = self.db.child(ruta_integrante).get(self.token).val()
            
            if not grupos_integrante or not isinstance(grupos_integrante, dict):
                grupos_integrante = {}
            
            grupos_integrante[id_grupo] = True
            self.db.child(ruta_integrante).update(grupos_integrante, self.token)
            
            return True, "Grupo creado correctamente"
        except Exception as e:
            print(f"Error al crear grupo: {e}")
            return False, str(e)
        
    async def eliminar_grupo(self, nombre_grupo):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario
            
            id_grupo_encontrar, datos_grupo_encontrar = await self.grupos_del_usuario_admin(nombre_grupo) # Buscar el grupo
            
            miembros = datos_grupo_encontrar.get("miembros", {}) # Obtener la lista de miembros

            # Eliminar el grupo de todos los miembros
            for id_miembro in miembros.keys():
                ruta_grupo_usuario = f"usuarios/{id_miembro}/grupos/{id_grupo_encontrar}" # Ruta completa al grupo específico del usuario
                
                grupo_ref = self.db.child(ruta_grupo_usuario).get(self.token).val() # Obtenemos la info de grupos_usuario
                if grupo_ref:
                    self.db.child(ruta_grupo_usuario).remove(self.token) # Eliminar la referencia del grupo de este usuario
            
            self.db.child(f"grupos/{id_grupo_encontrar}").remove(self.token) # Eliminar el grupo del nodo de grupos
            
            return True, "Grupo eliminado correctamente"
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)

    async def editar_grupo(self, nombre_grupo, nuevo_nombre_grupo):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario
            
            # Buscar el ID del grupo por nombre y verificar que sea admin
            id_grupo_encontrar, datos_grupo_encontrar = await self.grupos_del_usuario_admin(nombre_grupo)
        
            self.db.child(f"grupos/{id_grupo_encontrar}").update({"nombre": nuevo_nombre_grupo}, self.token) # Editar el nombre del grupo

            return True, "Grupo editado correctamente"
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)    

    async def mostrar_grupos(self):
        nombres_grupos = []  
        integrantes_con_nombres = [] 
        grupos_dentro_usuarios = None
        emails_usuarios_por_grupo = []

        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario

            # Obtener todos los grupos y usuarios
            grupos = await self.buscar_grupos()
            usuarios = self.db.child("usuarios").get(self.token).val()
            emails_usuarios = []

            grupos_dentro_usuarios = await self.page.shared_preferences.get("grupos")
        
            if grupos_dentro_usuarios is None:
                print("No hay grupos guardados en shared_preferences")
                return [], [], [], False
            
            # Si es string pasar a JSON
            if isinstance(grupos_dentro_usuarios, str):
                try:
                    grupos_dentro_usuarios = json.loads(grupos_dentro_usuarios)
                except:
                    grupos_dentro_usuarios = {}

            # Asegurar que es un diccionario
            if not isinstance(grupos_dentro_usuarios, dict):
                grupos_dentro_usuarios = {}        

            for id_grupo, datos_grupo in grupos.items():
                if id_grupo in grupos_dentro_usuarios:
                    nombres_grupos.append(datos_grupo.get("nombre", "Sin nombre"))
                    
                    # Obtener integrantes
                    nombres_integrantes = []
                    emails_usuarios = [] 
                    miembros = datos_grupo.get("miembros", {})
                    
                    if isinstance(miembros, dict):
                        for id_integrante in miembros.keys():
                            nombre_usuario = usuarios[id_integrante].get("nombre", id_integrante)
                            email_usuario = usuarios[id_integrante].get("email", id_integrante)
                            nombres_integrantes.append(nombre_usuario)
                            emails_usuarios.append(email_usuario)
                    
                    integrantes_con_nombres.append(nombres_integrantes)
                    emails_usuarios_por_grupo.append(emails_usuarios)
            
            if not nombres_grupos:
                return [], [], [], False
            return nombres_grupos, integrantes_con_nombres, emails_usuarios_por_grupo, True
        except Exception as e:
            print(f"Error al mostrar grupos: {e}")
            return [], [], [], False
            
    async def agregar_participante(self, nombre_grupo, nuevo_integrante):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario

            usuarios = self.db.child("usuarios").get(self.token).val()
            id_grupo_encontrar, datos_grupo_encontrar = await self.grupos_del_usuario_admin(nombre_grupo) # Buscar el ID del grupo por nombre y verificar que sea admin
            miembros = datos_grupo_encontrar.get("miembros", {}) # Obtener los miembros
            
            # Verificar que miembros sea un diccionario
            if not isinstance(miembros, dict):
                miembros = {}

            id_integrante = None
            datos_usuario_encontrar = None
            for id_usuario, datos_usuario in usuarios.items():
                if datos_usuario.get("email") == nuevo_integrante:
                    id_integrante = id_usuario
                    datos_usuario_encontrar = datos_usuario
                    break    
            
            if not id_integrante:
                return False, f"No se encontró el usuario con email {nuevo_integrante}"

            # Verificar si ya existe
            if id_integrante in miembros:
                return False, "El integrante ya está en el grupo"
            miembros[id_integrante] = True # Añadir el nuevo integrante

            grupos_integrante = datos_usuario_encontrar.get("grupos", {})    
            # Verificar que grupos_integrante sea un diccionario
            if not isinstance(grupos_integrante, dict):
                grupos_integrante = {}
            
            grupos_integrante[id_grupo_encontrar] = True
            
            # Actualizar usando el ID del grupo
            self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token)
            self.db.child(f"usuarios/{id_integrante}/grupos").update(grupos_integrante, self.token)
            
            return True, "Integrante añadido correctamente"
        except Exception as e:
            print(f"Error al añadir participante: {e}")
            return False, str(e)
        
    async def eliminar_participante(self, nombre_grupo, email_integrante):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario
                        
            id_grupo_encontrar, datos_grupo_encontrar = await self.grupos_del_usuario_admin(nombre_grupo) # Buscar el ID del grupo por nombre y verificar que sea admin
            
            # Verificar que sea admin
            if datos_grupo_encontrar.get("admin") != self.id_usuario:
                return False, "Solo el administrador puede eliminar participantes"
            
            # Obtener miembros
            miembros = datos_grupo_encontrar.get("miembros", {})
            
            if not isinstance(miembros, dict):
                miembros = {}
            
            usuarios = self.db.child("usuarios").get(self.token).val()
            id_integrante_eliminar = None
            for id_usuario, datos_usuario in usuarios.items():
                if datos_usuario.get("email") == email_integrante:
                    id_integrante_eliminar = id_usuario
                    break
            
            if not id_integrante_eliminar:
                return False, f"No se encontró el integrante '{email_integrante}'"
            
            # No permitir eliminar al admin
            if id_integrante_eliminar == self.id_usuario:
                return False, "No puedes eliminarte a ti mismo del grupo"
            
            # Eliminar del diccionario de miembros
            if id_integrante_eliminar not in miembros:
                return False, "El integrante no está en el grupo"
            
            del miembros[id_integrante_eliminar]
            self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token) # Actualizar en Firebase
            ruta_usuario = f"usuarios/{id_integrante_eliminar}/grupos/{id_grupo_encontrar}" 
            self.db.child(ruta_usuario).remove(self.token) # Eliminar referencia del grupo en el usuario eliminado
            
            return True, "Integrante eliminado correctamente"
        except Exception as e:
            print(f"Error al eliminar participante: {e}")
            return False, str(e)    