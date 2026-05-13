import json

class UsuarioService:
    def __init__(self, page, firebase_service):
            self.page = page
            self.fb = firebase_service
            self.db = firebase_service.db
            self.id_usuario = None
            self.token = None

    # funcion para actualizar los datos del usuario
    async def actualizar_datos(self, datos_actualizados):
        try:
            self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            self.token = await self.page.shared_preferences.get("token")

            try:
                self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados, self.token)
            except Exception as e:
                # al dar error comprobamos si es problema del token
                nuevo_token = await self.fb.comprobar_error(e)
                if nuevo_token:
                    # volemos a intentarlo con el nuevo token
                    self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados, nuevo_token)
                    print("Datos actualizados")
                else:
                    raise e # si no es error de token o no se puede refrescar devolvemos el error original
            
            # guardamos los datos en el dispositivo    
            for clave, valor in datos_actualizados.items():
                val_str = str(valor).lower() if isinstance(valor, bool) else str(valor) # convertimos todo a str porque shared preferences no adminte booleanos ni diccionarios
                await self.page.shared_preferences.set(clave, val_str)
                print("Datos actualizados en el dispositivo")
            return True, "Datos actualizados"
        except Exception as e:
            print(f"Error al actualizar: {e}")
            return False, str(e)

    # funcion para que se sincronice con los datos que hay firebase 
    async def sincronizar (self):

        try:
            self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            self.token = await self.page.shared_preferences.get("token")
            # self.token = "token_inventado_para_fallar" # esta linea es para comprobar que funciona el refresh token
            if self.id_usuario and self.token:
                try:
                    infor = self.db.child("usuarios").child(self.id_usuario).get(self.token).val()   
                except Exception as e:
                    nuevo_token = await self.fb.comprobar_error(e)
                    if nuevo_token:
                        infor = self.db.child("usuarios").child(self.id_usuario).get(nuevo_token).val()
                    else:
                        print("Error al sincronizar")
                        return

                if infor:
                    datos_a_guardar = { # diccionario de las cosas que queremos guardar en el dispositivo
                        "nombre": infor.get("nombre", ""),
                        "apellidos": infor.get("apellidos", ""),
                        "email": infor.get("email", ""),
                        "telefono": infor.get("telefono", ""),
                        "pais": infor.get("pais", ""),
                        "localidad": infor.get("localidad", ""),
                        "color_avatar": infor.get("color_avatar", "#1A6AFE"),
                        "compartir_ubicacion": infor.get("compartir_ubicacion", "false")
                    }

                    # sincronizamos los grupos en el caso de que tenga
                    if "grupos" in infor:
                        datos_a_guardar["grupos"] = json.dumps(infor.get("grupos", {}))

                    # guardamos todo a la vez
                    for clave, valor in datos_a_guardar.items():
                        await self.page.shared_preferences.set(clave, str(valor))
                    print("Sincronizado con firebase")
                else:
                    print("No hay informacion de este usuario en la base de datos")
        except Exception as e:
            print(f"Error al sincronizar: {e}")