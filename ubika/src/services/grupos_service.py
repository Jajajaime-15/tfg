from datetime import datetime
import json

class GruposService:
    def __init__(self, page, firebase_service):
        self.page = page
        self.fb = firebase_service # instanciamos firebase, su bbdd y la autenticacion
        self.auth = firebase_service.auth
        self.db = firebase_service.db
        self.id_usuario = None
        self.token = None
        self.todos_los_grupos_usuarios = None
        self.todos_los_usuarios = None

    #Funcion para buscar todos los grupos y reutilizarla en el resto de funciones
    async def buscar_grupos(self):
        try:
            todos_los_grupos = self.db.child("grupos").get(self.token).val() or {} # Obtener todos los grupos
            return todos_los_grupos
        except Exception as e:
            # si da error miramos si es de token
            nuevo_token = await self.fb.comprobar_error(e)
            if nuevo_token:
                self.token = nuevo_token
                todos_los_grupos = self.db.child("grupos").get(self.token).val() or {}
                return todos_los_grupos
            
            print(f"Error al buscar grupos: {e}")
            return {}

    #Funcion donde buscamos los y devolvemos los grupos del usuario es admin
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

    # Función donde refrescamos los datos del usuario
    async def cargar_datos_usuario(self):
        self.id_usuario = await self.page.shared_preferences.get("id_usuario")
        self.token = await self.page.shared_preferences.get("token")

        if self.id_usuario and self.token:
            try:
                self.todos_los_grupos_usuarios = self.db.child("usuarios").child(self.id_usuario).child("grupos").get(self.token).val()
                self.todos_los_usuarios = self.db.child("usuarios").get(self.token).val()
                await self.actualizar_grupos_preferences()
            except Exception as e:
                # si da error miramos si es de token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    self.todos_los_grupos_usuarios = self.db.child("usuarios").child(self.id_usuario).child("grupos").get(self.token).val()
                    self.todos_los_usuarios = self.db.child("usuarios").get(self.token).val()
                    await self.actualizar_grupos_preferences()
                else:
                    print(f"Error al cargar datos del usuario: {e}")
        else:
            print("No se pudo cargar el ID de usuario o el token")    

    # Función donde actualizamos la información de shared_preferences para que aparezca al cambiar de usuario
    async def actualizar_grupos_preferences(self):
        try:
            if self.todos_los_grupos_usuarios is None:
                grupos_actualizados = {}
            else:
                grupos_actualizados = self.todos_los_grupos_usuarios

            await self.page.shared_preferences.set("grupos", json.dumps(grupos_actualizados))
        except Exception as e:
            print(f"Error al sincronizar grupos: {e}")        

    # Función donde creamos los grupos 
    async def crear_grupo(self, nombre_grupo, integrante):
        try:
            await self.cargar_datos_usuario()  # Cargar datos del usuario

            id_nuevo_integrante = None
            for id_usuario, datos_usuario in self.todos_los_usuarios.items():
                if datos_usuario.get("email") == integrante:
                    id_nuevo_integrante = id_usuario
                    break

            if not id_nuevo_integrante:
                return False, "USER_NOT_FOUND"    

            miembros = {self.id_usuario: True, id_nuevo_integrante: True}

            info_grupo = {
                "admin": self.id_usuario,
                "nombre": nombre_grupo,
                "miembros": miembros,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            try:
                resultado = self.db.child("grupos").push(info_grupo, self.token) # Guardar en nodo "grupos"
                id_grupo = resultado["name"]  
                self.db.child(f"usuarios/{self.id_usuario}/grupos").update({id_grupo: True}, self.token)
                self.db.child(f"usuarios/{id_nuevo_integrante}/grupos").update({id_grupo: True}, self.token)
            except Exception as e:
                # si da error miramos si es de token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    resultado = self.db.child("grupos").push(info_grupo, self.token) # Guardar en nodo "grupos"
                    id_grupo = resultado["name"]  
                    self.db.child(f"usuarios/{self.id_usuario}/grupos").update({id_grupo: True}, self.token)
                    self.db.child(f"usuarios/{id_nuevo_integrante}/grupos").update({id_grupo: True}, self.token)

            return True, "Grupo creado correctamente"
        except Exception as e:
            print(f"Error al crear grupo: {e}")
            return False, str(e)

    # Función donde eliminamos los grupos
    async def eliminar_grupo(self, nombre_grupo):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario

            id_grupo_encontrar, datos_grupo_encontrar = await self.grupos_del_usuario_admin(nombre_grupo) # Buscar el grupo
            if not id_grupo_encontrar:
                return False, datos_grupo_encontrar

            miembros = datos_grupo_encontrar.get("miembros", {}) # Obtener la lista de miembros
            try:
                # Eliminar el grupo de todos los miembros
                for id_miembro in miembros.keys():
                    self.db.child(f"usuarios/{id_miembro}/grupos/{id_grupo_encontrar}").remove(self.token)

                self.db.child(f"grupos/{id_grupo_encontrar}").remove(self.token) # Eliminar el grupo del nodo de grupos
                self.db.child(f"ubicaciones/{id_grupo_encontrar}").remove(self.token) # eliminamos de ubicaciones
            except Exception as e:
                # si da error miramos si es de token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    for id_miembro in miembros.keys():
                        self.db.child(f"usuarios/{id_miembro}/grupos/{id_grupo_encontrar}").remove(self.token)

                    self.db.child(f"grupos/{id_grupo_encontrar}").remove(self.token) # Eliminar el grupo del nodo de grupos
                    self.db.child(f"ubicaciones/{id_grupo_encontrar}").remove(self.token) # eliminamos de ubicaciones

            return True, "Grupo eliminado correctamente"
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)

    # Función donde editamos los grupos
    async def editar_grupo(self, nombre_grupo, nuevo_nombre_grupo):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario

            # Buscar el ID del grupo por nombre y verificar que sea admin
            id_grupo_encontrar, datos_grupo_encontrar = await self.grupos_del_usuario_admin(nombre_grupo)

            try:
                self.db.child(f"grupos/{id_grupo_encontrar}").update({"nombre": nuevo_nombre_grupo}, self.token) # Editar el nombre del grupo
            except Exception as e:
                # si hay error miramos si es de token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    self.db.child(f"grupos/{id_grupo_encontrar}").update({"nombre": nuevo_nombre_grupo}, self.token) # Editar el nombre del grupo

            return True, "Grupo editado correctamente"
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False, str(e)    

    # Función para mostrar grupos
    async def mostrar_grupos(self):
        nombres_grupos = []  
        integrantes_con_nombres = [] 
        grupos_dentro_usuarios = {}
        emails_usuarios_por_grupo = []
        id_admins = []

        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario

            # Obtener todos los grupos y usuarios
            grupos = await self.buscar_grupos()
            try:
                usuarios = self.db.child("usuarios").get(self.token).val() or {}
            except Exception as e:
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    usuarios = self.db.child("usuarios").get(self.token).val() or {}

            emails_usuarios = []

            grupos_dentro_usuarios = await self.page.shared_preferences.get("grupos")
            if grupos_dentro_usuarios is None:
                print("No hay grupos guardados en shared_preferences")
                return [], [], [], [], False

            # Si es string pasar a JSON
            if isinstance(grupos_dentro_usuarios, str):
                try:
                    grupos_dentro_usuarios = json.loads(grupos_dentro_usuarios)
                except:
                    grupos_dentro_usuarios = {}

            # Asegurar que es un diccionario
            if not isinstance(grupos_dentro_usuarios, dict):
                grupos_dentro_usuarios = {}        

            if grupos: # comprobamos que existen grupos
                for id_grupo, datos_grupo in grupos.items():
                    if id_grupo in grupos_dentro_usuarios:
                        nombres_grupos.append(datos_grupo.get("nombre", "Sin nombre"))
                        id_admins.append(datos_grupo.get("admin", ""))

                        # Obtener integrantes
                        nombres_integrantes = []
                        emails_usuarios = [] 
                        miembros = datos_grupo.get("miembros", {})

                        if isinstance(miembros, dict):
                            for id_integrante in miembros.keys():
                                datos_usuario = usuarios.get(id_integrante,{})
                                nombre_usuario = datos_usuario.get("nombre", "")
                                email_usuario = datos_usuario.get("email", "")
                                nombres_integrantes.append(nombre_usuario)
                                emails_usuarios.append(email_usuario)

                        integrantes_con_nombres.append(nombres_integrantes)
                        emails_usuarios_por_grupo.append(emails_usuarios)

            if not nombres_grupos:
                return [], [], [], [], True
            return nombres_grupos, integrantes_con_nombres, emails_usuarios_por_grupo, id_admins, True
        except Exception as e:
            print(f"Error al mostrar grupos: {e}")
            return [], [], [], [], False

    # Función para añadir participante al grupo
    async def agregar_participante(self, nombre_grupo, nuevo_integrante):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario

            try:
                usuarios = self.db.child("usuarios").get(self.token).val()
            except Exception as e:
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
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
                return False, "EMAIL_NOT_FOUND"
            
            # Verificar si ya existe
            if id_integrante in miembros:
                return False, "El integrante ya está en el grupo"
            miembros[id_integrante] = True # Añadir el nuevo integrante

            grupos_integrante = datos_usuario_encontrar.get("grupos", {})    
            # Verificar que grupos_integrante sea un diccionario
            if not isinstance(grupos_integrante, dict):
                grupos_integrante = {}

            grupos_integrante[id_grupo_encontrar] = True

            try:
                # Actualizar usando el ID del grupo
                self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token)
                self.db.child(f"usuarios/{id_integrante}/grupos").update(grupos_integrante, self.token)
            except Exception as e:
                # si da error miramos si es de token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token)
                    self.db.child(f"usuarios/{id_integrante}/grupos").update(grupos_integrante, self.token)
            return True, "Integrante añadido correctamente"
        except Exception as e:
            print(f"Error al añadir participante: {e}")
            return False, str(e)

    # Función para eliminar integrantes del grupo
    async def eliminar_participante(self, nombre_grupo, email_integrante):
        try:
            await self.cargar_datos_usuario() # Cargar datos del usuario

            # buscamos el grupo y comrpobamos si somos o no admin [0]-admin [1]-no admin
            resultado = await self.grupos_del_usuario_admin(nombre_grupo)
            if resultado[0] is False:
                return False, resultado[1]

            id_grupo_encontrar, datos_grupo_encontrar = resultado

            # Obtener miembros
            miembros = datos_grupo_encontrar.get("miembros", {})
            usuarios = self.db.child("usuarios").get(self.token).val()

            # buscamos el id del miembro que queremos eliminar
            lista_ids = [id for id, datos in usuarios.items() if datos.get("email") == email_integrante]
            id_integrante_eliminar = lista_ids[0] if lista_ids else None

            if not id_integrante_eliminar: # comprobamos que existe el id
                return False, f"No se encontró el usuario {email_integrante}"
            if id_integrante_eliminar == self.id_usuario: # comrpobamos que no seamos el admin
                return False, "Operación no permitida: El administrador no puede eliminarse a sí mismo."
            if id_integrante_eliminar not in miembros: # comprobamos si sigue el id en los miembros del grupo
                return False, "El usuario ya no pertenece a este grupo"

            # eliminamos en firebase
            del miembros[id_integrante_eliminar]

            try:
                self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token) # Actualizar en Firebase
                ruta_usuario = f"usuarios/{id_integrante_eliminar}/grupos/{id_grupo_encontrar}" 
                self.db.child(ruta_usuario).remove(self.token) # Eliminar referencia del grupo en el usuario eliminado
                self.db.child(f"ubicaciones/{id_grupo_encontrar}/{id_integrante_eliminar}").remove(self.token) # quitamos del mapa de ese grupo
            except Exception as e:
                # si hay error comprobamos si es de token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    self.db.child(f"grupos/{id_grupo_encontrar}").update({"miembros": miembros}, self.token) # Actualizar en Firebase
                    ruta_usuario = f"usuarios/{id_integrante_eliminar}/grupos/{id_grupo_encontrar}" 
                    self.db.child(ruta_usuario).remove(self.token) # Eliminar referencia del grupo en el usuario eliminado
                    self.db.child(f"ubicaciones/{id_grupo_encontrar}/{id_integrante_eliminar}").remove(self.token) # quitamos del mapa de ese grupo
            return True, "Integrante eliminado correctamente"
        except Exception as e:
            print(f"Error al eliminar participante: {e}")
            return False, str(e)

    # funcion para salir del grupo si no eres admin
    async def abandonar_grupo(self, grupo):
        try:
            await self.cargar_datos_usuario()
            encontrar_id_grupo = None
            encontrar_datos = None
            todos_los_grupos = await self.buscar_grupos()
            encontrado = False

            if todos_los_grupos:
                for id_grupo, datos_grupo in todos_los_grupos.items():
                    if not encontrado:
                        if datos_grupo.get("nombre") == grupo:
                            encontrar_id_grupo = id_grupo
                            encontrar_datos = datos_grupo
                            encontrado = True
            if not encontrado:
                return False, f"El grupo {grupo} no se ha encontrado"

            # quitamos al usuario de la lista de miembros del grupo
            miembros = encontrar_datos.get("miembros", {})
            if isinstance(miembros, str):
                miembros = {}
            if self.id_usuario in miembros:
                del miembros[self.id_usuario]
                self.db.child(f"grupos/{encontrar_id_grupo}/miembros").set(miembros, self.token) # actualizamos la informacion del grupo en firebase

            try:
                # quitamos el grupo de la lista de grupos del usuario
                mi_grupo = f"usuarios/{self.id_usuario}/grupos/{encontrar_id_grupo}"
                self.db.child(mi_grupo).remove(self.token)
                self.db.child(f"ubicaciones/{encontrar_id_grupo}/{self.id_usuario}").remove(self.token) # quitamos del mapa de ese grupo
            except Exception as e:
                # si da error miramos si es de token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    self.token = nuevo_token
                    self.db.child(f"grupos/{encontrar_id_grupo}/miembros").set(miembros, self.token)
                    self.db.child(f"usuarios/{self.id_usuario}/grupos/{encontrar_id_grupo}").remove(self.token)
                    self.db.child(f"ubicaciones/{encontrar_id_grupo}/{self.id_usuario}").remove(self.token)
            return True, f"Has salido del grupo {grupo}"
        except Exception as e:
            print(f"Error al salir del grupo: {e}")
            return False, str(e)