import asyncio
from utils.mostrar_avisos import mostrar_aviso

class GruposController:
    def __init__(self, page, grupos_service, vista=None):
        self.page = page
        self.grupos_service = grupos_service
        self.vista = vista

    async def crear_grupo(self, nombre, integrante):
        mostrar_aviso(self.page, self.vista, "")
        self.page.update()

        datos = [nombre.value, integrante.value]

        if not all (datos):
            mostrar_aviso(self.page, self.vista, "Todos los campos son obligatorios")
        else:
            creado, aviso = await self.grupos_service.crear_grupo(nombre.value, integrante.value)
            if creado:
                mostrar_aviso(self.page, self.vista, "Grupo creado correctamente", color = "#1A6AFE")
                await self.grupos_service.cargar_datos_usuario()
                self.page.update()
                await asyncio.sleep(1.5) # esperamos para que el usuario tenga tiempo de leer el mensaje
                await self.page.push_route("/home")
                # actualizamos la vista con el nuevo grupo
                if self.vista and hasattr(self.vista, "actualizar_tarjetas_grupos"):
                    await self.vista.actualizar_tarjetas_grupos()            
            else:
                error_crear = str(aviso).upper()
                if "NOT_FOUND" in error_crear:
                    mostrar_aviso(self.page, self.vista, "El email no está registrado")
                else:
                    mostrar_aviso(self.page, self.vista, f"Error: {aviso}")

        self.page.update()

    async def eliminar_grupo(self, nombre_grupo):
        mostrar_aviso(self.page, self.vista, "")
        self.page.update()

        if not nombre_grupo:
            mostrar_aviso(self.page, self.vista, "El nombre del grupo es obligatorio")
        else:
            borrado, aviso = await self.grupos_service.eliminar_grupo(nombre_grupo)
            if borrado:
                mostrar_aviso(self.page, self.vista, "Grupo eliminado", color="#1A6AFE")
                if self.vista and hasattr(self.vista, "actualizar_tarjetas_grupos"):
                    await self.vista.actualizar_tarjetas_grupos() 
            else:
                mostrar_aviso(self.page, self.vista, "No eres el administrador de este grupo")

        self.page.update()    

    async def editar_grupo(self, nombre_grupo_actual, nuevo_nombre_grupo):
        mostrar_aviso(self.page, self.vista, "")
        self.page.update()

        if not nombre_grupo_actual or not nuevo_nombre_grupo:
            mostrar_aviso(self.page, self.vista, "El nombre es obligatorio")   
            return False 

        editado, aviso = await self.grupos_service.editar_grupo(nombre_grupo_actual, nuevo_nombre_grupo)
        if editado:
            mostrar_aviso(self.page, self.vista, "Nombre de grupo actualizado", color="#1A6AFE")
            self.page.update()
            await asyncio.sleep(1.5)
            return True
        else:
            mostrar_aviso(self.page, self.vista, f"Error: {aviso}")
            return False

    async def mostrar_grupos(self):
        mostrar_aviso(self.page, self.vista, "")
        self.page.update()

        datos_grupo, integrantes, emails, id_admins, aviso = await self.grupos_service.mostrar_grupos()

        if aviso is False:
            mostrar_aviso(self.page, self.vista, "Error al cargar los grupos. Revisa tu conexión.")
            return [], [], [], []

        if not datos_grupo:
            mostrar_aviso(self.page, self.vista, "Aún no perteneces a ningún grupo", color="#1A6AFE")
        else:
            mostrar_aviso(self.page, self.vista, "")

        self.page.update()
        return datos_grupo, integrantes, emails, id_admins

    async def agregar_participante(self, nombre_grupo, nuevo_integrante):
        mostrar_aviso(self.page, self.vista, "")
        self.page.update()

        datos = [nombre_grupo, nuevo_integrante]

        if not all (datos):
            mostrar_aviso(self.page, self.vista, "Todos los campos son obligatorios")
        elif "@" not in nuevo_integrante or "." not in nuevo_integrante:
            mostrar_aviso(self.page, self.vista, "Introduce un email válido")
        else:
            anyadido, aviso = await self.grupos_service.agregar_participante(nombre_grupo, nuevo_integrante)
            if anyadido:
                mostrar_aviso(self.page, self.vista, "Integrante añadido", color="#1A6AFE")
                if self.vista and hasattr(self.vista, "actualizar_tarjetas_grupos"):
                    await self.vista.actualizar_tarjetas_grupos()
            else:
                error_agregar = str(aviso).upper()
                if "NOT_FOUND" in error_agregar:
                    mostrar_aviso(self.page, self.vista, "Email no registrado")
                elif "ALREADY" in error_agregar or "EXISTE" in error_agregar:
                    mostrar_aviso(self.page, self.vista, "Ya pertenece al grupo")
                else:
                    mostrar_aviso(self.page, self.vista, "Error al añadir")

        self.page.update()    

    async def eliminar_participante(self, nombre_grupo, email_integrante):
        mostrar_aviso(self.page, self.vista, "")
        self.page.update() # FALTA
        
        await self.grupos_service.cargar_datos_usuario()

        # comprobamos primero si somos el propio usuario
        if email_integrante.lower().strip() ==self.grupos_service.id_usuario.lower().strip():
            mostrar_aviso(self.page, self.vista, "No puedes eliminarte. Eres el administrador.")
            self.page.update()
            await asyncio.sleep(1.5)
            return False

        # si no es el propio usuario realizamos la eliminacion
        eliminado, aviso = await self.grupos_service.eliminar_participante(nombre_grupo, email_integrante)

        if eliminado:
            mostrar_aviso(self.page, self.vista, "Participante eliminado correctamente", color="#1A6AFE")
            self.page.update()
            await asyncio.sleep(1.5)
            if self.vista and hasattr(self.vista, "actualizar_tarjetas_grupos"):
                await self.vista.actualizar_tarjetas_grupos()
        else:
            error_eliminar_participante = str(aviso).upper()
            if "NOT_FOUND" in error_eliminar_participante:
                mostrar_aviso(self.page, self.vista, "Usuario no encontrado en la base de datos")
            else:
                mostrar_aviso(self.page, self.vista, aviso)

        self.page.update()
        return eliminado

    async def abandonar_grupo(self, grupo):
        mostrar_aviso(self.page, self.vista, "")
        self.page.update()

        exito, aviso = await self.grupos_service.abandonar_grupo(grupo)
        if exito:
            mostrar_aviso(self.page, self.vista, "Has salido del grupo", color="#1A6AFE")
            await asyncio.sleep(1.2)
            return True
        else:
            mostrar_aviso(self.page, self.vista, "Error al salir")
            return False

    def obtener_id(self):
        return self.grupos_service.id_usuario