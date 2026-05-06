import flet as ft # type: ignore
import asyncio

class UsuarioController:
    def __init__ (self, page, usuario_service, vista=None, ajustes_controller=None):
        self.page = page
        self.service = usuario_service
        self.vista = vista
        self.ajustes_controller = ajustes_controller

    async def cargar_perfil(self):
        await self.service.sincronizar() # sincronizamos los datos del usuario por si acaso cada vez que se carga el perfil
        # cogemos los datos que estan guardados en el dispositivo
        nombre = await self.page.shared_preferences.get("nombre") or ""
        apellidos = await self.page.shared_preferences.get("apellidos") or ""
        email = await self.page.shared_preferences.get("email") or ""
        telefono = await self.page.shared_preferences.get("telefono") or ""
        pais = await self.page.shared_preferences.get("pais") or ""
        localidad = await self.page.shared_preferences.get("localidad") or ""

        # datos del formulario
        self.vista.nombre_input.value = nombre
        self.vista.nombre_input.read_only = True # no dejamos que el nombre se pueda cambiar
        self.vista.apellidos_input.value = apellidos
        self.vista.telefono_input.value = telefono
        self.vista.pais_input.value = pais
        self.vista.localidad_input.value = localidad
        
        # extraemos la primera letra del nombre y la ponemos en mayusculas para el avatar
        if nombre and len(nombre.strip())>0: # evitamos que de error si el nombre llega vacío
            self.vista.inicial_texto.value = nombre[0].upper()
        else:
            self.vista.inicial_texto.value = "?"

        # datos en la parte de arriba (cabecera)
        self.vista.usuario.value = f"{nombre} {apellidos}".strip()
        self.vista.email.value = email

        # obtenemos el color de avatar que tiene elegido el usuario en la anterior sesion
        color_guardado = await self.page.shared_preferences.get("color_avatar")
        if color_guardado:
            self.vista.avatar.bgcolor=color_guardado
        else:
            self.vista.avatar.bgcolor="#1A6AFE"

        self.page.update()
    
    async def guardar_cambios(self,e):
        self.vista.btn_guardar.disabled = True # bloqueamos el botón para que no se pueda hacer clic mas de una vez
        self.vista.mensaje_error.value = ""
        self.page.update()

        # creamos el diccionario con los campos que se pueden modificar
        datos = {
            "apellidos":self.vista.apellidos_input.value,
            "telefono":self.vista.telefono_input.value,
            "pais":self.vista.pais_input.value,
            "localidad":self.vista.localidad_input.value
        }

        guardado, aviso = await self.service.actualizar_datos(datos)
        if guardado:
                self.vista.mensaje_error.value = "Datos actualizados"
                self.vista.mensaje_error.color = "green"
                # actualiza la cabecera si se cambia el apellio
                nombre = self.vista.nombre_input.value
                apellidos = self.vista.apellidos_input.value
                self.vista.usuario.value = f"{nombre} {apellidos}".strip()
                self.page.update()
                await asyncio.sleep(3) # Esperamos 3 segundos
                self.vista.mensaje_error.value = ""
                self.page.update()
        else:
                self.vista.mensaje_error.color = "red"
                error_guardado = str(aviso).upper()
                if "SESION_EXPIRADA" in error_guardado:
                    self.vista.mensaje_error.value = "Sesión caducada, vuelve a iniciar sesión"
                    self.page.update()
                    await asyncio.sleep(2)
                    await self.service.auth_s.cerrar_sesion()
                    self.page.router.reset_vistas() # # llamamos a la funcion que resetea la vista
                    self.page.index_navegacion = 0 # aseguramos que al iniciar sesion entre en grupos
                    self.page.go("/")
                elif "PERMISSION_DENIED" in error_guardado:
                    self.vista.mensaje_error.value = "No tienes permisos para modificar los datos"
                elif "NETWORK" in error_guardado or "CONNECTION" in error_guardado:
                    self.vista.mensaje_error.value = "Sin conexión."
                else:
                    self.vista.mensaje_error.value = "Error al guardar los datos"

        self.vista.btn_guardar.disabled = False # activamos el botón de nuevo
        self.page.update()

    # funcion para abrir los ajustes
    async def ajustes (self, e):
        # guardamos en memoria 2 que es la posición de Perfil en nuestra vista principal para así cuando demos a volver nos vuelva a perfil
        self.page.index_navegacion = 2 # no usamos shared_preferences porque solo se recuerda mientras que la sesion este activa, si cerramos la aplicacion desde la vista que sea siempre al abrirla vuelve a aparecer la principal con grupos
        await self.page.push_route("/settings")
        # se llama a la carga de los ajustes para que el switch tenga la ultima configuracion seleccionada
        if self.ajustes_controller:
            await self.ajustes_controller.cargar_ajustes()

    # funcion para abrir el menu
    async def mostrar_colores(self, e):
        # limpiamos el overlay para evitar duplicados
        if self.vista.lista_colores in self.page.overlay:
            self.page.overlay.remove(self.vista.lista_colores)

        self.page.overlay.append(self.vista.lista_colores) # añadimos de nuevo el overlay
        self.vista.lista_colores.open = True # mostramos el menu
        self.page.update()

    # funcion para seleccionar el color y guardarlo
    async def seleccionar_color(self, e):
        color_elegido = e.control.data
        self.vista.lista_colores.open = False # cerramos el menu
        self.vista.avatar.bgcolor = color_elegido # actualizamos el color del avatar
        self.page.update()

        datos = {"color_avatar":color_elegido} 
        await self.service.actualizar_datos(datos) # usamos la funcion de actualizar datos para guardarlo en firebase y Shared preferences

    ''' PENDIENTE DE BORRAR, EL ERROR DE QUE AL CERRAR SESIÓN Y ABRIR UNA NUEVA CARGUE LOS DATOS ANTIGUOS SE SOLUCIONA CON EL RESET_VISTA
    # función para que la vista de perfil limpie la información de la sesión anterior
    def limpiar_vista(self):
        if self.vista:
            self.vista.nombre_input.value = ""
            self.vista.apellidos_input.value = ""
            self.vista.telefono_input.value = ""
            self.vista.pais_input.value = ""
            self.vista.localidad_input.value = ""
            self.vista.inicial_texto.value = ""
            self.vista.usuario.value = ""
            self.vista.email.value = ""
            self.vista.avatar.bgcolor = "TRANSPARENT"
            print("Datos anteriores eliminados")'''