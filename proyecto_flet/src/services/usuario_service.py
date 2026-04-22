class UsuarioService:
    def __init__(self, page, firebase_service, auth_service):
            self.page = page
            self.fb = firebase_service
            self.auth_s = auth_service
            self.db = firebase_service.db
            self.id_usuario = None
            self.token = None

    # funcion para actualizar los datos del usuario
    async def actualizar_datos(self,datos_actualizados):
        try:
            # recuperamos el id del usuario y el token
            if not self.id_usuario:
                self.id_usuario = await self.page.shared_preferences.get("id_usuario")
            if not self.token:
                self.token = await self.page.shared_preferences.get("token")
            # intentamos actualizar los datos
            try:
                self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados, self.token)
            except Exception as e:
                print ("Token caducado")
                # llamamos a la funcion para actualizar el token
                if await self.actualizar_sesion():
                    try:
                        # volvemos a intentar actualizar los datos
                        self.db.child("usuarios").child(self.id_usuario).update(datos_actualizados,self.token)
                    except Exception as x:
                        print("Error después de actualizar el token")
                        return False, f"Error después de actualizar el token{x}"
                else:
                    print ("Sesion caducada")
                    return False, "Sesion caducada, inicia sesión de nuevo"
            # guardamos los datos en el dispositivo
            for clave, valor in datos_actualizados.items():
                await self.page.shared_preferences.set(clave,valor)
            print ("Datos actualizados")
            return True, "Datos actualizados"
        except Exception as e:
            print(f"Error: {e}")
            return False, str(e)