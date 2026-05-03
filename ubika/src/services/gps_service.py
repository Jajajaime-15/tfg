import flet as ft # para flet
import pyrebase # para firebase
import flet_geolocator as ftg # para la geolocalizacion
from threading import Thread # para los hilos
from database.config import config # las claves que tenemos en el .env
import asyncio

firebase = pyrebase.initialize_app(config) 
db = firebase.database() 

class GPSService:
    def __init__(self, page, firebase_service):
        self.page = page
        self.firebase = firebase_service # instanciamos firebase, su bbdd y la autenticacion
        self.db = self.firebase.db
        self.auth = self.firebase.auth
        self.yo = "jaime" # el propio usuario
        self.miembros_grupos = [] # una lista de los miembros de todos los grupos a los que pertenece el usuario
        self.grupos = db.child("usuarios").child(self.yo).child("grupos").get().val() 
        self.datos_miembros_cache = {} # diccionario para manejar los nombres y colores de los miembros para poder pintarlos en el mapa
        self.datos_usuario = { # lo mismo pero con los datos del propio usuario
            "nombre" : db.child("usuarios").child(self.yo).child("nombre").get().val(), 
            "color" : db.child("usuarios").child(self.yo).child("color_avatar").get().val()
        }

        self.actualizar_marcador_usuario = None # para conectar con el controlador y poder actualizar los marcadores en el mapa
        self.actualizar_marcador_miembros = None
        self.cola_miembros = None # la cola que nos permite conectar los hilos de pyrebase con el event loop de flet
        self.bucle = None # sera la referencia al event loop de flet para poder hacer llamadas seguras

        # recorremos los grupos a los que pertenece el usuario y cada miembro para guardarlos en la lista de miembros y poder evitar repetidos
        if self.grupos: # por si el usuario no esta todavia en ningun grupo
            for grupo in self.grupos.keys():
                miembros = db.child("grupos").child(grupo).child("miembros").get().val()
                for miembro in miembros.keys():
                    if miembro not in self.miembros_grupos and miembro != self.yo: 
                        self.miembros_grupos.append(miembro)
        
    # es la funcion que define la corutina que nos permite procesar lo que haya en la cola desde el event loop de flet de forma segura
    async def procesar_cola(self):
        while True:
            miembro, datos_miembro, lat, lon, timestamp = await self.cola_miembros.get() # la corrutina se puede pausar aqui si fuera necesario y reanudar en este punto cuando le toque
            if self.actualizar_marcador_miembros:
                self.actualizar_marcador_miembros(miembro, datos_miembro, lat, lon, timestamp) # indicamos el miembro, con su nombre y color y su localizacion para que el mapa lo pueda pintar

    # funcion para gestionar el cambio de ubicacion del usuario con geolocator tanto en firebase como en el mapa
    def cambio_ubicacion(self, cambio: ftg.GeolocatorPositionChangeEvent): # para el on position change del geolocator
        latitud = cambio.position.latitude
        longitud = cambio.position.longitude
        timestamp = str(cambio.position.timestamp)
        loc = {
            "latitud" : latitud,
            "longitud" : longitud,
            "timestamp" : timestamp
        }

        if self.grupos and self.page.platform == ft.PagePlatform.ANDROID: # para que solo escriba en Firebase desde el móvil, ya que escritorio no escribe la ubicacion correcta
            for grupo in self.grupos.keys(): # para escribir el cambio de posicion en todos los grupos a los que se pertenezca
                db.child("ubicaciones").child(grupo).child(self.yo).set(loc) # si se cambia la posicion la escribimos en la base de datos
        
        if self.actualizar_marcador_usuario: # solo en caso de que exista
            self.actualizar_marcador_usuario(self.datos_usuario, latitud, longitud, timestamp) # llamamos a la funcion del mapa para pintar el marcador propio personalizado cada vez que se actualice la posicion

    # funcion para solicitar que se active el permiso de ubicacion si no esta activado en la aplicacion
    async def permitir_ubicacion(self, geo):
        permiso_localizacion = await geo.get_permission_status() # comprobamos si esta habilitado el permiso de localizacion en el dispositivo
        
        if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE): # en caso de NO estar habilitado
            await geo.request_permission() # solicitamos permiso
            permiso_localizacion = await geo.get_permission_status() # comprobamos de nuevo

            if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE):
                self.page.add(ft.Text(f"Permisos de localización no habilitados"))
                return False # avisamos de que no han sido habilitados y hacemos que no se siga ejecutando la funcion
        
        return True # en caso de SI estar habilitado
    
    # funcion para obtener la posicion inicial del usuario
    async def posicion_inicial(self, geo):
        localizacion = await geo.get_current_position() # obtenemos la posicion actual del dispositivo

        latitud = localizacion.latitude
        longitud = localizacion.longitude
        timestamp = str(localizacion.timestamp) # el timestamp no es algo valido para el json asi que hay que convertirlo a string

        loc = {
            "latitud" : latitud,
            "longitud" : longitud,
            "timestamp" : timestamp 
        }

        try:
            if self.grupos and self.page.platform == ft.PagePlatform.ANDROID: # para que solo escriba en Firebase desde el móvil, ya que escritorio no escribe la ubicacion correcta
                for grupo in self.grupos.keys(): # para escribir la posicion inicial en todos los grupos a los que se pertenezca
                    db.child("ubicaciones").child(grupo).child(self.yo).set(loc) # para escribir los valores debemos marcar el nivel dentro de los json con los 'child' y 'set'
        except Exception as e:
            self.page.add(ft.Text(f"Error escritura Firebase: {e}"))
        
        return latitud, longitud, timestamp
    
    # funcion callback para usar el cambio de la ubicacion en los miembros de los grupos a los que pertenece el usuario
    def callback_miembro(self, miembro): # para identificar que miembro es
        def cambio_ubicacion_miembro(ubicacion_miembro): 
            if self.actualizar_marcador_miembros and ubicacion_miembro["data"]: # 'data' es la forma en la que llega la info de la ubicacion en el stream del listener
                lat = ubicacion_miembro["data"].get("latitud")
                lon = ubicacion_miembro["data"].get("longitud")
                timestamp = ubicacion_miembro["data"].get("timestamp")

                if miembro not in self.datos_miembros_cache: # comprobamos si el miembro esta en la cache
                    nombre_miembro = db.child("usuarios").child(miembro).child("nombre").get().val()
                    color_miembro = db.child("usuarios").child(miembro).child("color_avatar").get().val()
                    self.datos_miembros_cache[miembro] = {"nombre" : nombre_miembro, "color": color_miembro} # si no esta obtenemos sus datos de firebase para dibujar el marcador
                datos_miembro = self.datos_miembros_cache[miembro] # en cualquier caso obtenemos asi el nombre y el color que seran enviados al mapa

                if lat and lon and timestamp:
                    # metemos los datos en la cola creada para que no haya problemas con los hilos, es el event loop quien mete los datos a la cola cuando es seguro hacerlo
                    self.bucle.call_soon_threadsafe(self.cola_miembros.put_nowait, (miembro, datos_miembro, lat, lon, timestamp)) 
        return cambio_ubicacion_miembro
    
    # listener para recibir cada vez que haya un cambio en la ubicacion de un miembro de los grupos a los que pertenece el usuario, se inicia cada stream en un hilo para no bloquear el event loop
    def listener_ubicacion_miembros(self, miembro):
        if self.grupos:
            for grupo in self.grupos.keys():
                # el stream hace que escuchemos constantemente esta parte de realtime por si hay cambios y llamamos al callback
                db.child("ubicaciones").child(grupo).child(miembro).stream(self.callback_miembro(miembro)) 

    # funcion para configurar el geolocator segun el dispositivo en el que se use la app
    def configurar_geolocator(self):
        if self.page.platform == ft.PagePlatform.ANDROID:
            return ftg.GeolocatorAndroidConfiguration( # configuracion solo para dispositivos Android
                accuracy=ftg.GeolocatorPositionAccuracy.BEST, # declaramos el geolocator configurando su precision de localizacion como la mejor posible
                interval_duration=10000, # para que se actualice cada 10 segundos la posicion
                distance_filter=5, # para que se actualice al desplazarse cierta distancia, en este caso 5 metros
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
            return ftg.GeolocatorConfiguration( # configuracion para cualquier dispositivo que no sea Android
                accuracy=ftg.GeolocatorPositionAccuracy.BEST,
                distance_filter=5
            )

    # metodo principal que servira como orquestador de todo el gps
    async def gps(self, actualizar_marcador_usuario=None, actualizar_marcador_miembros=None): # recibe las funciones para actualizar los marcadores en tiempo real
        self.actualizar_marcador_usuario = actualizar_marcador_usuario
        self.actualizar_marcador_miembros = actualizar_marcador_miembros # declaramos la funcion del controller para que procesar cola la pueda usar
        self.cola_miembros = asyncio.Queue() # instanciamos la cola ahora que el event loop es el correcto
        self.bucle = asyncio.get_event_loop() # instanciamos el event loop de flet cuando ya ha sido iniciado

        # añade la corrutina a la lista de tareas que tiene pendientes el event loop de flet, la corrutina pasa a vivir en el event loop
        self.page.run_task(self.procesar_cola)

        geo = ftg.Geolocator(
            configuration=self.configurar_geolocator(), # la configuracion varia dependiendo del dispositivo
            on_position_change=self.cambio_ubicacion, # para llamar a un metodo que actualice cuando haya un cambio de posicion
            on_error=lambda e: None # mensaje de error que aparecera en la pantalla
        )

        if not await self.permitir_ubicacion(geo): # solicitamos el permiso de ubicacion
            return # para salir del programa si no se han concedido los permisos de ubicacion
        
        lat, lon, timestamp = await self.posicion_inicial(geo) # obtenemos la posicion actual del usuario
        
        if self.actualizar_marcador_usuario: 
            self.actualizar_marcador_usuario(self.datos_usuario, lat, lon, timestamp) # llamamos a la funcion del mapa para pintar el marcador propio personalizado con la posicion inicial

        for miembro in self.miembros_grupos:
            hilo_listener = Thread(target=self.listener_ubicacion_miembros, args=(miembro,)) # el listener va en un hilo para que pueda estar escuchando y no bloquee el programa, un hilo por miembro
            hilo_listener.daemon = True # para que muera el hilo siempre que se cierre la app
            hilo_listener.start()

        return lat, lon, geo # para poder dibujar la posicion inicial en el mapa y pasar el geo para añadirlo a la pagina desde el mapa en un Stack