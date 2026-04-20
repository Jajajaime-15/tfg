import flet as ft

class UserController:
    def __init__ (self,page,wrapper,vista=None):
        self.page = page
        self.wrapper = wrapper
        self.vista = vista

    async def cargar_perfil(self):
        # cogemos los datos que estan guardados en el dispositivo
        nombre = await self.page.shared_preferences.get("nombre")
        apellidos = await self.page.shared_preferences.get("apellidos")
        apellidos_comprobado = apellidos if apellidos else "" # con esta linea hacemos que si no rellena el apellido en la cabecera no aparezca None
        email = await self.page.shared_preferences.get("email")
        telefono = await self.page.shared_preferences.get("telefono")
        pais = await self.page.shared_preferences.get("pais")
        localidad = await self.page.shared_preferences.get("localidad")

        # datos del formulario
        self.vista.nombre_input.value = nombre
        self.vista.nombre_input.read_only = True # no dejamos que el nombre se pueda cambiar
        self.vista.apellidos_input.value = apellidos_comprobado
        self.vista.telefono_input.value = telefono if telefono else ""
        self.vista.pais_input.value = pais if pais else ""
        self.vista.localidad_input.value = localidad if localidad else ""
        # datos en la parte de arriba (cabecera)
        self.vista.usuario.value = f"{nombre} {apellidos_comprobado}".strip()
        self.vista.email.value = email
        
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
        guardado, aviso = await self.wrapper.actualizar_datos(datos)
        if guardado:
                self.vista.mensaje_error.value = "Datos actualizados"
                self.vista.mensaje_error.color = "green"
                # actualiza la cabecera si se cambia el apellio
                nombre = self.vista.nombre_input.value
                apellidos = self.vista.apellidos_input.value
                self.vista.usuario.value = f"{nombre} {apellidos}".strip()
                self.page.update()
        else:
                error_guardado = str(aviso).upper()
                if "INVALID_ID_TOKEN" in error_guardado or "EXPIRED" in error_guardado:
                    self.vista.mensaje_error.value = "Sesión caducada, vuelve a iniciar"
                elif "PERMISION_DENIED" in error_guardado:
                    self.vista.mensaje_error.value = "No tienes permisos para modificar los datos"
                elif "NETWORK" in error_guardado or "CONNECTION" in error_guardado:
                     self.vista.mensaje_error.value = "Sin conxión."
                else:
                    self.vista.mensaje_error.value = "Error al guardar los datos"
        
        self.vista.btn_guardar.disabled = False # activamos el botón de nuevo
        self.page.update()

    # funcion para abrir los ajustes (PDTE. DE CONFIGURAR, A FALTA DE CREAR LOS AJUSTES)
    async def ajustes (self,e):
         self.page.index_navegacion = 2 # POR QUE NO GUARDAR EN SHARED_PREFERENCES AQUI TMB?
         await self.page.push_route("/settings")
