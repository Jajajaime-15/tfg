import asyncio

class GruposController:
    def __init__(self, page, grupos_service, vista=None):
        self.page = page
        self.grupos_service = grupos_service
        self.vista = vista

    async def crear_grupo(self, nombre, integrante, mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre.value, integrante.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = "red"
        else:
            creado, aviso = await self.grupos_service.crear_grupo(nombre.value, integrante.value)
            if creado:
                mensaje.value = "Grupo creado correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2) # esperamos para que el usuario tenga tiempo de leer el mensaje
                # actualizamos la vista con el nuevo grupo
                if self.vista:
                    await self.vista.actualizar_tarjetas_grupos()
                await self.page.push_route("/home")
            else:
                mensaje.value = f"Error al crear grupo: {aviso}"
                mensaje.color = "red"

        self.page.update()

    async def eliminar_grupo(self, nombre_grupo, mensaje):
        mensaje.value = ""
        self.page.update()

        if not nombre_grupo:
            mensaje.value = "El nombre del grupo es obligatorio"
            mensaje.color = "red"
        else:
            borrado, aviso = await self.grupos_service.eliminar_grupo(nombre_grupo)
            if borrado:
                mensaje.value = "Grupo eliminado correctamente"
                mensaje.color = "green"
                self.page.update()
                # refrescamos las tarjetas
                if self.vista:
                    await self.vista.actualizar_tarjetas_grupos()
                mensaje.value = ""  
            else:
                mensaje.value = f"No puedes eliminar el grupo si no eres el administrador"
                mensaje.color = "red"

        self.page.update()    

    async def editar_grupo(self, nombre_grupo_actual, nuevo_nombre_grupo, mensaje):
        mensaje.value = ""
        self.page.update()

        if not nombre_grupo_actual or not nuevo_nombre_grupo:
            mensaje.value = "El nombre del grupo es obligatorio"
            mensaje.color = "red"
            self.page.update()     
            return False 

        editado, aviso = await self.grupos_service.editar_grupo(nombre_grupo_actual, nuevo_nombre_grupo)
        if editado:
            mensaje.value = "Grupo editado correctamente"
            mensaje.color = "green"
            self.page.update()
            await asyncio.sleep(1.5)
            mensaje.value = ""
            return True
        else:
            mensaje.value = f"Error al editar grupo: {aviso}"
            mensaje.color = "red"
            self.page.update() 
            return False

    async def mostrar_grupos(self, mensaje):
        mensaje.value = ""
        self.page.update()

        datos_grupo, integrantes, emails, id_admins, aviso = await self.grupos_service.mostrar_grupos()

        if aviso is False:
            mensaje.value = f"Error: {integrantes}"
            mensaje.color = "red"
            self.page.update()
            return [], [], [], []  # Retornar listas vacías en caso de error

        if datos_grupo:
            mensaje.value = ""
            mensaje.color = "green"
        else:
            mensaje.value = "Todavia no perteneces a ningún grupo"
            mensaje.color = "orange"

        self.page.update()
        return datos_grupo, integrantes, emails, id_admins

    async def agregar_participante(self, nombre_grupo, nuevo_integrante, mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre_grupo, nuevo_integrante]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = "red"
        else:
            anyadido, aviso = await self.grupos_service.agregar_participante(nombre_grupo, nuevo_integrante)
            if anyadido:
                mensaje.value = "Participante añadido correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                # refrescamos la vista para que aparezca el nuevo miembro en la tarjeta
                if self.vista:
                    await self.vista.actualizar_tarjetas_grupos()
            else:
                mensaje.value = f"Error al añadir integrante en el grupo"
                mensaje.color = "red"

        self.page.update()    

    async def eliminar_participante(self, nombre_grupo, email_integrante, mensaje):
        mensaje.value = ""
        self.page.update()
        
        await self.grupos_service.cargar_datos_usuario()

        # comprobamos primero si somos el propio usuario
        if email_integrante.lower().strip() ==self.grupos_service.id_usuario.lower().strip():
            mensaje.value = "No puedes eliminarte a ti mismo del grupo. Usa la opción 'Salir del grupo'."
            mensaje.color = "orange" # Usamos naranja para una advertencia de lógica
            self.page.update()
            await asyncio.sleep(1.5)
            return False

        # si no es el propio usuario realizamos la eliminacion
        eliminado, aviso = await self.grupos_service.eliminar_participante(nombre_grupo, email_integrante)

        if eliminado:
            mensaje.value = "Integrante eliminado correctamente"
            mensaje.color = "green"
        else:
            mensaje.value = aviso # mostramos el mensaje que viene desde el service
            mensaje.color = "red"

        self.page.update()
        return eliminado

    async def abandonar_grupo(self, grupo, mensaje):
        mensaje.value = ""
        self.page.update()

        if not grupo:
            mensaje.value = "No se ha encontrado el grupo"
            mensaje.color = "red"
            self.page.update()
            return False

        exito, aviso = await self.grupos_service.abandonar_grupo(grupo)
        if exito:
            mensaje.value = "Has salido del grupo"
            mensaje.color = "green"
            self.page.update()
            await asyncio.sleep(1.5)
            return True
        else:
            mensaje.value = f"Error al salir del grupo: {aviso}"
            mensaje.color = "red"
            self.page.update()
            return False

    def obtener_id(self):
        return self.grupos_service.id_usuario