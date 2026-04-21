class AjustesService:
    def __init__(self, page, firebase_service, auth_service):
        self.page = page
        self.fb = firebase_service
        self.auth_s = auth_service

    # funcion para cambiar la contraseña estando conectado    
    async def cambiar_psw(self,nueva_psw):
        try:
            self.token = await self.page.shared_preferences.get("token")
            # obtenemos el token si no está en memoria
            if not self.token:
                return False, "TOKEN_EXPIRED"            
            # actualizamos la contraseña
            self.auth.change_password(self.token,nueva_psw)
            print("Contraseña actualizada")
            return True, "Contraseña actualizada"
        except Exception as e:
            mensaje = str(e).upper()
            print(f"DEBUG: Error detectado en Firebase: {mensaje}")
            if "CREDENTIAL_TOO_OLD" in mensaje or "SENSITIVE_OPERATION" in mensaje:
                return False, "REQUIRES_RECENT_LOGIN" 
            # si el token está caducado, refrescamos el token
            if await self.actualizar_sesion():
                try:
                    self.token = await self.page.shared_preferences.get("token")
                    self.auth.change_password(self.token,nueva_psw)
                    return True, "Contraseña actualizada"
                except:
                    return False, "REQUIRES_RECENT_LOGIN"
            return False, "Error desconocido"
        
    # funcion para eliminar la cuenta y los datos de dicha cuenta
    async def borrar_cuenta(self):
        try:
            if not self.id_usuario:
                self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            if not self.token:
                self.token = await self.page.shared_preferences.get("token")

            # borramos toda la informacion de la base de datos (de Realtime)
            self.db.child("usuarios").child(self.id_usuario).remove(self.token)
            # borramos el usuario de Authentication
            self.auth.delete_user_account(self.token)
            # una vez eliminado cerramos sesión
            await self.cerrar_sesion()

            print("Cuenta eliminada")
            return True, "La cuenta ha sido eliminada"
        except Exception as e:
            print(f"Error al borrar la cuenta: {e}")
            return False, "Error al eliminar cuenta, inténtalo de nuevo iniciando sesión"
        