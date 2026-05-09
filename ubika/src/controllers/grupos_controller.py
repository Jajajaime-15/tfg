import asyncio

class GruposController:
    def __init__(self, page, grupos_service):
        self.page = page
        self.grupos_service = grupos_service

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
                await self.page.push_route("/home")
            else:
                mensaje.value = f"Error al crear grupo: {aviso}"
                mensaje.color = "red"

        self.page.update()

    async def eliminar_grupo(self, nombre_grupo, mensaje):
        print(f"GroupController.eliminar_grupo llamado con: {nombre_grupo}")  # PRINT DEBUG
        mensaje.value = ""
        self.page.update()

        # Si nombre_grupo es un objeto o string
        if hasattr(nombre_grupo, 'value'):
            nombre = nombre_grupo.value
        else:
            nombre = nombre_grupo

        if not nombre:
            mensaje.value = "El nombre del grupo es obligatorio"
            mensaje.color = "red"
        else:
            borrado, aviso = await self.grupos_service.eliminar_grupo(nombre)
            if borrado:
                mensaje.value = "Grupo eliminado correctamente"
                mensaje.color = "green"
                self.page.update()
                mensaje.value = ""  
            else:
                mensaje.value = f"Error al eliminar grupo: {aviso}"
                mensaje.color = "red"

        self.page.update()    

    async def editar_grupo(self, nombre_grupo_actual, nuevo_nombre_grupo, mensaje):
        mensaje.value = ""
        self.page.update()

        # Verificar si nombre_grupo es un objeto o string
        if hasattr(nombre_grupo_actual, 'value'):
            nombre_actual = nombre_grupo_actual.value
        else:
            nombre_actual = nombre_grupo_actual

        if hasattr(nuevo_nombre_grupo, 'value'):
            nombre_nuevo = nuevo_nombre_grupo.value
        else:
            nombre_nuevo = nuevo_nombre_grupo    

        if not nombre_actual or not nombre_nuevo:
            mensaje.value = "El nombre del grupo es obligatorio"
            mensaje.color = "red"
            self.page.update()     
            return False 
        
        editado, aviso = await self.grupos_service.editar_grupo(nombre_actual, nombre_nuevo)
        if editado:
            mensaje.value = "Grupo editado correctamente"
            mensaje.color = "green"
            self.page.update()
            await asyncio.sleep(1.5)
            mensaje.value = ""  
            self.page.update() 
            return True
        else:
            mensaje.value = f"Error al editar grupo: {aviso}"
            mensaje.color = "red"
            self.page.update() 
            return False
        
    async def mostrar_grupos(self, mensaje):
        mensaje.value = ""
        self.page.update()
        
        datos_grupo, integrantes, emails, aviso = await self.grupos_service.mostrar_grupos()
        
        if aviso is False:
            mensaje.value = f"Error: {integrantes}"
            mensaje.color = "red"
            self.page.update()
            return [], []  # Retornar listas vacías en caso de error
        
        if datos_grupo:
            mensaje.value = ""
            mensaje.color = "green"
        else:
            mensaje.value = "No tienes grupos aún"
            mensaje.color = "orange"
        
        self.page.update()
        return datos_grupo, integrantes, emails
    
    async def anyadir_participante(self, nombre_grupo, nuevo_integrante, mensaje):
        mensaje.value = ""
        self.page.update()
        
        datos = [nombre_grupo, nuevo_integrante]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = "red"
        else:
            anyadido, aviso = await self.grupos_service.anyadir_participante(nombre_grupo, nuevo_integrante)
            if anyadido:
                mensaje.value = "Participante añadido correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                mensaje.value = ""
            else:
                mensaje.value = f"Error al añadir participante: {aviso}"
                mensaje.color = "red"

        self.page.update()    

    async def eliminar_participante(self, nombre_grupo, email_integrante, mensaje):
        mensaje.value = ""
        self.page.update()
        
        eliminado, aviso = await self.grupos_service.eliminar_participante(nombre_grupo, email_integrante)
        if eliminado:
            mensaje.value = "Integrante eliminado correctamente"
            mensaje.color = "green"
            self.page.update()
            await asyncio.sleep(2)
            mensaje.value = ""
        else:
            mensaje.value = f"Error al eliminar integrante: {aviso}"
            mensaje.color = "red"
        
        self.page.update()
        return eliminado    