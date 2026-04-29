import json

class AjustesService:
    def __init__(self, page, firebase_service, auth_service):
        self.page = page
        self.fb = firebase_service
        self.auth_s = auth_service
        self.auth = firebase_service.auth
        self.db = firebase_service.db
        self.id_usuario = None
        self.token = None

    # funcion para cambiar la contraseña estando conectado    
    async def cambiar_psw(self,nueva_psw):
        try:
            self.token = await self.page.shared_preferences.get("token")
            # obtenemos el token si no está en memoria
            if not self.token:
                return False, "Token caducado"            
            # actualizamos la contraseña
            self.auth.change_password(self.token, nueva_psw)
            print("Contraseña actualizada")
            return True, "Contraseña actualizada"
        except Exception as e:
            mensaje = str(e).upper()
            if "CREDENTIAL_TOO_OLD" in mensaje or "SENSITIVE_OPERATION" in mensaje:
                print("Sesión caducada, vuelve a logearte")
                return False, "Sesión caducada, vuelve a iniciar"
            # si el token está caducado, refrescamos el token
            if await self.auth_s.actualizar_sesion():
                try:
                    self.token = await self.page.shared_preferences.get("token")
                    self.auth.change_password(self.token,nueva_psw)
                    print("Contraseña actualizada")
                    return True, "Contraseña actualizada"
                except:
                    print("Sesión caducada, vuelve a logearte")
                    return False, "Sesión caducada, vuelve a iniciar"
            return False, str(e)
        
    # funcion para eliminar la cuenta y los datos de dicha cuenta
    async def borrar_cuenta(self):
        grupos = {}
        try:
            self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            self.token = await self.page.shared_preferences.get("token")
            # obtenemos el grupo o grupos al que pertenece
            grupos_guardados = await self.page.shared_preferences.get("grupos")
            grupos = json.loads(grupos_guardados) if grupos_guardados else {} 
            if self.id_usuario and self.token:
                # borramos toda la informacion de la base de datos (de Realtime)
                self.db.child("usuarios").child(self.id_usuario).remove(self.token)
                # borramos la última posición guardada del usuario en todos los grupos para que no se quede marcada al eliminar la cuenta
                if grupos:
                    for id_grupo in grupos.keys():
                        self.db.child("ubicaciones").child(id_grupo).child(self.id_usuario).remove(self.token)
                # borramos el usuario de Authentication
                self.auth.delete_user_account(self.token)
                # una vez eliminado cerramos sesión
                await self.auth_s.cerrar_sesion()
                print("Cuenta eliminada")
                return True, "La cuenta ha sido eliminada"
            print ("No hay una sesión activa")
            return False, "No hay una sesión activa"
        except Exception as e:
            mensaje = str(e).upper()
            if "CREDENTIAL_TOO_OLD" in mensaje or "SENSITIVE_OPERATION" in mensaje:
                print("Sesión caducada, vuelve a logearte")
                return False, "Sesión caducada, vuelve a iniciar"
            if await self.auth_s.actualizar_sesion():
                try:
                    self.token = await self.page.shared_preferences.get("token")
                    self.db.child("usuarios").child(self.id_usuario).remove(self.token)
                    if grupos:
                        for id_grupo in grupos.keys():
                            self.db.child("ubicaciones").child(id_grupo).child(self.id_usuario).remove(self.token)
                    self.auth.delete_user_account(self.token)
                    await self.auth_s.cerrar_sesion()
                    return True, "La cuenta ha sido eliminada"
                except:
                    print("Sesión caducada, vuelve a logearte")
                    return False, "Sesión caducada, vuelve a iniciar"
            return False, str(e)