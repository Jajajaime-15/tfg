import flet as ft # para flet
import pyrebase # para firebase
import flet_geolocator as ftg # para la geolocalizacion
from threading import Thread # para los hilos
from database.config import config_keys # las claves que tenemos en el .env

firebase = pyrebase.initialize_app(config_keys) # iniciamos firebase
db = firebase.database() # instanciamos la base de datos y la autenticacion
auth = firebase.auth()

class GPSService:
    def __init__(self, page):
        self.page = page
        self.yo = "jaime" # el propio usuario
        self.miembros_grupos = [] # una lista de los miembros de todos los grupos a los que pertenece el usuario
        self.grupos = db.child("usuarios").child(self.yo).child("grupos").get().val() 
        self.datos_miembros_cache = {} # diccionario para manejar los nombres y colores de los miembros para poder pintarlos en el mapa
        self.datos_usuario = { # lo mismo pero con los datos del propio usuario
            "nombre" : db.child("usuarios").child(self.yo).child("nombre").get().val(), 
            "color" : db.child("usuarios").child(self.yo).child("color_avatar").get().val()
        }

        # recorremos los grupos a los que pertenece el usuario y cada miembro para guardarlos en la lista de miembros y poder evitar repetidos
        if self.grupos: # por si el usuario no esta todavia en ningun grupo
            for grupo in self.grupos.keys():
                miembros = db.child("grupos").child(grupo).child("miembros").get().val()
                for miembro in miembros.keys():
                    if miembro not in self.miembros_grupos and miembro != self.yo: # QUIZAS TENEMOS QUE HACER QUE ESTO SE HAGA POR UN ID POR SI ACASO HAY DOS PERSONAS EN GRUPOS DISTINTOS CON EL MISMO NOMBRE
                        self.miembros_grupos.append(miembro)

    async def gps(self, actualizar_marcador_usuario=None, actualizar_marcador_miembros=None): # recibe las funciones para actualizar los marcadores en tiempo real
        # funcion para gestionar el cambio de ubicacion del usuario con geolocator tanto en firebase como en el mapa
        def cambio_ubicacion(cambio: ftg.GeolocatorPositionChangeEvent): # para el on position change del geolocator
            latitud = cambio.position.latitude
            longitud = cambio.position.longitude
            timestamp = str(cambio.position.timestamp)
            loc = {
                "latitud" : latitud,
                "longitud" : longitud,
                "timestamp" : timestamp
            }

            if self.grupos:
                for grupo in self.grupos.keys(): # para escribir el cambio de posicion en todos los grupos a los que se pertenezca
                    db.child("ubicaciones").child(grupo).child(self.yo).set(loc) # si se cambia la posicion la escribimos en la base de datos
            
            if actualizar_marcador_usuario: # solo en caso de que exista
                actualizar_marcador_usuario(self.datos_usuario, latitud, longitud, timestamp) # llamamos a la funcion del mapa para pintar el marcador propio personalizado cada vez que se actualice la posicion

        # funcion para solicitar que se active el permiso de ubicacion si no esta activado en la aplicacion
        async def permitir_ubicacion(geo):
            permiso_localizacion = await geo.get_permission_status() # comprobamos si esta habilitado el permiso de localizacion en el dispositivo
            
            if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE): # en caso de NO estar habilitado
                await geo.request_permission() # solicitamos permiso
                permiso_localizacion = await geo.get_permission_status() # comprobamos de nuevo

                if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE):
                    self.page.add(ft.Text(f"Permisos de localización no habilitados"))
                    return False # avisamos de que no han sido habilitados y hacemos que no se siga ejecutando la funcion
            
            return True # en caso de SI estar habilitado
        
        # funcion para obtener la posicion inicial del usuario
        async def posicion_inicial(geo):
            localizacion = await geo.get_current_position() # obtenemos la posicion actual del dispositivo

            latitud = localizacion.latitude
            longitud = localizacion.longitude
            timestamp = str(localizacion.timestamp)

            loc = {
                "latitud" : latitud,
                "longitud" : longitud,
                "timestamp" : timestamp # el timestamp no es algo valido en json asi que hay que convertirlo a string
            }

            try:
                if self.grupos:
                    for grupo in self.grupos.keys(): # para escribir la posicion inicial en todos los grupos a los que se pertenezca
                        db.child("ubicaciones").child(grupo).child(self.yo).set(loc) # para escribir los valores debemos marcar el nivel dentro de los json con los 'child' y 'set'
            except Exception as e:
                self.page.add(ft.Text(f"Error escritura Firebase: {e}"))
            
            return latitud, longitud, timestamp
        
        # funcion callback para usar el cambio de la ubicacion en los miembros de los grupos a los que pertenece el usuario
        def callback_miembro(miembro): # para identificar que miembro es
            def cambio_ubicacion_miembro(ubicacion_miembro): 
                if actualizar_marcador_miembros and ubicacion_miembro["data"]: # 'data' es la forma en la que llega la info de la ubicacion en el stream del listener
                    lat = ubicacion_miembro["data"].get("latitud")
                    lon = ubicacion_miembro["data"].get("longitud")
                    timestamp = ubicacion_miembro["data"].get("timestamp")

                    if miembro not in self.datos_miembros_cache: # comprobamos si el miembro esta en la cache
                        nombre_miembro = db.child("usuarios").child(miembro).child("nombre").get().val()
                        color_miembro = db.child("usuarios").child(miembro).child("color_avatar").get().val()
                        self.datos_miembros_cache[miembro] = {"nombre" : nombre_miembro, "color": color_miembro} # si no esta obtenemos sus datos de firebase para dibujar el marcador
                    datos_miembro = self.datos_miembros_cache[miembro] # en cualquier caso obtenemos asi el nombre y el color que seran enviados al mapa

                    if lat and lon and timestamp:
                        actualizar_marcador_miembros(miembro, datos_miembro, lat, lon, timestamp) # indicamos el miembro, con su nombre y color y su localizacion para que el mapa lo pueda pintar
            return cambio_ubicacion_miembro

        # listener para recibir cada vez que haya un cambio en la ubicacion de un miembro de los grupos a los que pertenece el usuario
        def listener_ubicacion_miembros(miembro):
            if self.grupos:
                for grupo in self.grupos.keys():
                    # el stream hace que escuchemos constantemente esta parte de realtime por si hay cambios y llamamos al callback
                    db.child("ubicaciones").child(grupo).child(miembro).stream(callback_miembro(miembro)) 
        
        # funcion para cargar la posicion inicial de los miembros, que sera su ultima posicion conocida, antes de entrar en el stream del listener
        def posicion_inicial_miembros():
            for miembro in self.miembros_grupos:
                if not self.grupos:
                    break
                for grupo in self.grupos.keys():
                    try:
                        posicion = db.child("ubicaciones").child(grupo).child(miembro).get().val()
                        if posicion:
                            latitud = posicion.get("latitud")
                            longitud = posicion.get("longitud")
                            timestamp = posicion.get("timestamp")
                        
                            if latitud and longitud and timestamp:
                                if miembro not in self.datos_miembros_cache:
                                    nombre_miembro = db.child("usuarios").child(miembro).child("nombre").get().val()
                                    color_miembro = db.child("usuarios").child(miembro).child("color_avatar").get().val()
                                    self.datos_miembros_cache[miembro] = {"nombre" : nombre_miembro, "color": color_miembro}

                                if actualizar_marcador_miembros:
                                    datos_miembro = self.datos_miembros_cache[miembro]
                                    actualizar_marcador_miembros(miembro, datos_miembro, latitud, longitud, timestamp)
                    except Exception as e:
                        print(f"Error al cargar la posicion inicial del miembro {miembro}: {e}")

        if self.page.platform == ft.PagePlatform.ANDROID:
            configuracion = ftg.GeolocatorAndroidConfiguration( # configuracion solo para dispositivos Android
                accuracy=ftg.GeolocatorPositionAccuracy.BEST, # declaramos el geolocator configurando su precision de localizacion como la mejor posible
                foreground_notification_config=ftg.ForegroundNotificationConfiguration( # para mostrar una notificacion de la ubicacion que persista con la app en segundo plano
                    notification_title="Ubika",
                    notification_text="Compartiendo la ubicación en tiempo real...",
                    notification_enable_wake_lock=True, # para que no se apague en ningun momento ni se pierda la conexion a internet
                    notification_enable_wifi_lock=True, 
                    notification_set_ongoing=True, # para que se mantenga atento el dispositivo constantemente a los cambios
                    notification_channel_name="Ubicación en segundo plano"
                )
            )
        else:
            configuracion = ftg.GeolocatorConfiguration( # configuracion para cualquier dispositivo que no sea Android
                accuracy=ftg.GeolocatorPositionAccuracy.BEST
            )

        geo = ftg.Geolocator(
            configuration=configuracion, # la configuracion varia dependiendo del dispositivo
            on_position_change=cambio_ubicacion, # para llamar a un metodo que actualice cuando haya un cambio de posicion
            on_error=lambda e: None # mensaje de error que aparecera en la pantalla
        )

        if not await permitir_ubicacion(geo): # solicitamos el permiso de ubicacion
            return # para salir del programa si no se han concedido los permisos de ubicacion
        
        lat, lon, timestamp = await posicion_inicial(geo) # obtenemos la posicion actual del usuario
        
        if actualizar_marcador_usuario: 
            actualizar_marcador_usuario(self.datos_usuario, lat, lon, timestamp) # llamamos a la funcion del mapa para pintar el marcador propio personalizado con la posicion inicial

        # para cargar la ultima posicion registrada de los miembros antes de iniciar el listener de sus posiciones
        posicion_inicial_miembros()

        for miembro in self.miembros_grupos:
            hilo_listener = Thread(target=listener_ubicacion_miembros, args=(miembro,)) # el listener va en un hilo para que pueda estar escuchando y no bloquee el programa, un hilo por miembro
            hilo_listener.daemon = True # para que muera el hilo siempre que se cierre la app
            hilo_listener.start()

        return lat, lon, geo # para poder dibujar la posicion inicial en el mapa y pasar el geo para añadirlo a la pagina desde el mapa en un Stack