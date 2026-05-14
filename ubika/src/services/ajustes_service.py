import json

class AjustesService:
    def __init__(self, page, firebase_service):
        self.page = page
        self.fb = firebase_service
        self.auth = firebase_service.auth
        self.db = firebase_service.db
        self.id_usuario = None
        self.token = None

    # funcion para cambiar la contraseña estando conectado    
    async def cambiar_psw(self, nueva_psw):
        try: # obtenemos el token si no está en memoria
            self.token = await self.page.shared_preferences.get("token")
            if not self.token:
                return False, "Token caducado"            
            self.auth.change_password(self.token, nueva_psw) # actualizamos la contraseña
            print("Contraseña actualizada")
            return True, "Contraseña actualizada"
        except Exception as e:
            nuevo_token = await self.fb.comprobar_error(e) # comprobamos si es error de token
            if nuevo_token:
                self.token = nuevo_token
                try:
                    # volvemos a intentarlo con el nuevo token
                    self.auth.change_password(self.token,nueva_psw)
                    print("Contraseña actualizada despues de actualizar")
                    return True, "Contraseña actualizada"
                except Exception as e2:
                    print(f"Error despues de actualizar: {e2}")
                    return False, "Sesicón caducada, tienes que volver a iniciar"
                
            mensaje = str(e).upper()
            if "CREDENTIAL_TOO_OLD" in mensaje or "SENSITIVE_OPERATION" in mensaje:
                print("Sesión caducada, vuelve a iniciar")
                return False, str(e)
        
    # funcion para eliminar la cuenta y los datos de dicha cuenta
    async def borrar_cuenta(self):
        grupos = {}
        try:
            self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            self.token = await self.page.shared_preferences.get("token")
            grupos_guardados = await self.page.shared_preferences.get("grupos") # obtenemos los grupos a los que pertenece
            grupos = json.loads(grupos_guardados) if grupos_guardados else {} 

            if self.id_usuario and self.token:
                try:
                    # borramos toda la informacion de la base de datos (de Realtime)
                    self.db.child("usuarios").child(self.id_usuario).remove(self.token)
                    # borramos la última posición guardada del usuario en todos los grupos para que no se quede marcada al eliminar la cuenta
                    if grupos:
                        for id_grupo in grupos.keys():
                            self.db.child("ubicaciones").child(id_grupo).child(self.id_usuario).remove(self.token)
                    # borramos el usuario de Authentication
                    self.auth.delete_user_account(self.token)
                    # una vez eliminado cerramos sesión
                except Exception as e:
                    # si da error miramos si es de token
                    nuevo_token = await self.fb.comprobar_error(e)
                    if nuevo_token:
                        self.token = nuevo_token
                        self.db.child("usuarios").child(self.id_usuario).remove(self.token)
                        if grupos:
                            for id_grupo in grupos.keys():
                                self.db.child("ubicaciones").child(id_grupo).child(self.id_usuario).remove(self.token)
                        self.auth.delete_user_account(nuevo_token)
                    else:
                        raise e # devolvemos el error
                print("Cuenta eliminada")
                return True, "Cuenta eliminada"
            return False, "No hay sesion activa"
        except Exception as e:
            mensaje = str(e).upper()
            if "CREDENTIAL_TOO_OLD" in mensaje or "SENSITIVE_OPERATION" in mensaje:
                print("Se necesita iniciar sesion de nuevo")
                return False, "Sesión caducada, vuelve a iniciar"
            
            return False, str(e)