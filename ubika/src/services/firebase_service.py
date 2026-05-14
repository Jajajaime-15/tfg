import pyrebase # para firebase en python # type: ignore
from database.config import config # las claves que tenemos en el .env

class FirebaseService:
    def __init__(self, page):
        self.page = page
        try:
            self.firebase = pyrebase.initialize_app(config)
            self.auth = self.firebase.auth()
            self.db = self.firebase.database()
            self.id_usuario = None
            self.token = None
            print("Conectado a firebase") # print para comprobar que no hay problema a la hora de conectarse
        except Exception as e:
            print("Error al conectarse a firebase")

    # funcion para actualizar el token (refreshtoken)
    async def actualizar_sesion(self):
        try:
            # cogemeos el refreshtoken guardado
            token_refresh = await self.page.shared_preferences.get("refresh_token")
            if token_refresh:
                # actualizamos sesion con el metodo .refresh
                nuevo = self.auth.refresh(token_refresh)
                # cogemos el nuevo idToken y lo guardamos en el dispositivo
                nuevo_token = nuevo.get("idToken")
                if nuevo_token:
                    # guardamos es el nuevo idToken para las peticiones
                    await self.page.shared_preferences.set("token",nuevo_token)
                    # comprobamos si firebase a renovado el refresh_token y lo guardamos tambien en el dispositivo
                    if nuevo.get("refreshToken"):
                        await self.page.shared_preferences.set("refresh_token", nuevo.get("refreshToken"))
                    print("Token refrescado")
                    return nuevo_token # devolvemos el token nuevo para usarlo directamente
                return None
        except Exception as e:
            print(f"Error al refrescar la sesion: {e}")
            return None
    
    # funcion para comprobar si el error es por token caducado
    async def comprobar_error(self,e):
        mensaje_error = str(e).upper()

        # comprobamos los errores ed token caducado
        if "401" in mensaje_error or "EXPIRED" in mensaje_error or "INVALID_ID_TOKEN" in mensaje_error:
            print("Error de token. Actualizamos sesion")
            token_nuevo = await self.actualizar_sesion() # como es un error de token llamamos a la funcion para actualizarlo
            return token_nuevo
        return None # devolvemos none si no es error de token
