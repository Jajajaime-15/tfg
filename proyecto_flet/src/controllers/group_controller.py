import flet as ft
import asyncio

class GroupController:
    def __init__(self,page,wrapper):
        self.page = page
        self.wrapper = wrapper

    async def crear_grupo (self,nombre,integrante,mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre.value, integrante.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
        else:
            creado, aviso = await self.wrapper.crear_grupo(nombre.value, integrante.value)
            if creado:
                # provisional para confirmar en pantalla el registro
                mensaje.value = "Grupo creado correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2) # POR QUE? PONED AUNQUE SEA UN COMENTARIO PARA SABER POR QUE SE HACE ESTO
                await self.page.push_route("/") # ESTO NO LLEVARIA A LA PANTALLA DE LOGIN EN VEZ DE A LA DE HOME? LO TIENES ASI EN TODAS LAS ACCIONES
                '''# uso de snack_bar para mostrar el aviso de registrado y que desaparezca solo NO ME APARECE
                self.page.snack_bar = ft.SnackBar(ft.Text("Grupo creado correctamente"))
                self.page.snack_bar.open = True'''
            else:
                mensaje.value = f"Error al crear grupo: {aviso}"
                mensaje.color = "red"


        self.page.update()

    async def eliminar_grupo (self,nombre,mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
        else:
            borrado, aviso = await self.wrapper.eliminar_grupo(nombre.value)
            if borrado:
                # provisional para confirmar en pantalla el registro
                mensaje.value = "Grupo eliminado correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                await self.page.push_route("/")
                '''# uso de snack_bar para mostrar el aviso de registrado y que desaparezca solo NO ME APARECE
                self.page.snack_bar = ft.SnackBar(ft.Text("Grupo creado correctamente"))
                self.page.snack_bar.open = True'''
            else:
                mensaje.value = f"Error al crear grupo: {aviso}"
                mensaje.color = "red"


        self.page.update()    

        
    async def mostrar_grupos(self, mensaje):
        mensaje.value = ""
        self.page.update()
        
        datos_grupo, integrantes, aviso = await self.wrapper.mostrar_grupos()
        
        if aviso is False:
            mensaje.value = f"Error: {integrantes}"
            mensaje.color = "red"
            self.page.update()
            return [], []  # Retornar listas vacías en caso de error
        
        if datos_grupo:
            mensaje.value = f"Se encontraron {len(datos_grupo)} grupos"
            mensaje.color = "green"
        else:
            mensaje.value = "No tienes grupos aún"
            mensaje.color = "orange"
        
        self.page.update()
        return datos_grupo, integrantes
    
    
    async def anyadir_participante(self, nombre_grupo, nuevo_integrante, mensaje):
        mensaje.value = ""
        self.page.update()

        datos = [nombre_grupo.value, nuevo_integrante.value]

        if not all (datos):
            mensaje.value = "Todos los campos son obligatorios"
        else:
            anyadido, aviso = await self.wrapper.anyadir_participante(nombre_grupo.value, nuevo_integrante.value)
            if anyadido:
                # provisional para confirmar en pantalla el registro
                mensaje.value = "Participante añadido correctamente"
                mensaje.color = "green"
                self.page.update()
                await asyncio.sleep(2)
                await self.page.push_route("/")
            else:
                mensaje.value = f"Error al crear grupo: {aviso}"
                mensaje.color = "red"


        self.page.update()    