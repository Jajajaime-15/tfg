import flet as ft # para flet
import pyrebase # para firebase
import flet_geolocator as ftg # para la geolocalizacion
import flet_map as ftm # para el mapa
from threading import Thread # para los hilos
from db.config import config_keys # las claves que tenemos en el .env

firebase = pyrebase.initialize_app(config_keys) # iniciamos firebase
db = firebase.database() # instanciamos la base de datos y la autenticacion
auth = firebase.auth()

async def gps(page: ft.Page, actualizar_marcador_usuario=None, actualizar_marcador_miembros=None): # recibe la pagina y para actualizar el marcador en tiempo real
    #page.add(ft.Text("Firebase conectado"))
    yo = "jaime" # el propio usuario
    #yo = db.child("").child("")
    miembros_grupos = [] # una lista de los miembros de todos los grupos a los que pertenece el usuario
    grupos = db.child("usuarios").child(yo).child("grupos").get().val() 

    # recorremos los grupos a los que pertenece el usuario y cada miembro para guardarlos en la lista de miembros y poder evitar repetidos
    for grupo in grupos.keys():
        miembros = db.child("grupos").child(grupo).child("miembros").get().val()
        for miembro in miembros.keys():
            if miembro not in miembros_grupos: # QUIZAS TENEMOS QUE HACER EL NOMBRE DE LOS USUARIOS UNICO O QUE ESTO SE HAGA POR UN ID
                miembros_grupos.append(miembro)

    # funcion para gestionar el cambio de ubicacion del geolocator tanto en firebase como en el mapa
    def cambio_ubicacion(cambio: ftg.GeolocatorPositionChangeEvent): # para el on position change del geolocator
        latitud = cambio.position.latitude
        longitud = cambio.position.longitude
        timestamp = cambio.position.timestamp
        loc = {
            "latitud" : latitud,
            "longitud" : longitud,
            "timestamp" : str(timestamp)
        }

        for grupo in grupos.keys(): # para escribir el cambio de posicion en todos los grupos a los que se pertenezca
            db.child("ubicaciones").child(grupo).child(yo).set(loc) # si se cambia la posicion la escribimos en la base de datos
        
        if actualizar_marcador_usuario: # solo en caso de que exista
            actualizar_marcador_usuario(latitud, longitud) # llamamos a la funcion del mapa para pintar el marcador propio cada vez que se actualice la posicion
        
        #page.add(ft.Text(f"Cambio ubicacion OK: {latitud} {longitud} {timestamp}"))

    # funcion para solicitar que se active el permiso de ubicacion si no esta activado en la aplicacion
    async def permitir_ubicacion(geo):
        permiso_localizacion = await geo.get_permission_status() # comprobamos si esta habilitado el permiso de localizacion en el dispositivo
        
        if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE): # en caso de NO estar habilitado
            await geo.request_permission() # solicitamos permiso
            permiso_localizacion = await geo.get_permission_status() # comprobamos de nuevo

            if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE):
                page.add(ft.Text(f"Permisos de localización no habilitados"))
                return False # avisamos de que no han sido habilitados y hacemos que no se siga ejecutando la funcion
        
        return True
    
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
            for grupo in grupos.keys(): # para escribir la posicion inicial en todos los grupos a los que se pertenezca
                db.child("ubicaciones").child(grupo).child(yo).set(loc) # para escribir los valores debemos marcar el nivel dentro de los json con los 'child' y 'set'
            #page.add(ft.Text(f"Escritura OK"))
        except Exception as e:
            page.add(ft.Text(f"Error escritura Firebase: {e}"))
        
        return latitud, longitud
    
    # funcion callback para usar el cambio de la ubicacion en los miembros de los grupos a los que pertenece el usuario
    def callback_miembro(miembro): # para identificar que miembro es
        def cambio_ubicacion_miembro(ubicacion_miembro): 
            if actualizar_marcador_miembros and ubicacion_miembro["data"]: # 'data' es la forma en la que llega la info de la ubicacion en el stream del listener
                lat = ubicacion_miembro["data"].get("latitud")
                lon = ubicacion_miembro["data"].get("longitud")
                if lat and lon:
                    actualizar_marcador_miembros(miembro, lat, lon) # indicamos el miembro y su localizacion para que el mapa lo pueda pintar
        return cambio_ubicacion_miembro

    # listener para recibir cada vez que haya un cambio en la ubicacion de un miembro de los grupos a los que pertenece el usuario
    def listener(miembro):
        for grupo in grupos.keys():
            # el stream hace que escuchemos constantemente esta parte de realtime por si hay cambios y llamamos al callback
            db.child("ubicaciones").child(grupo).child(miembro).stream(callback_miembro(miembro)) 


    geo = ftg.Geolocator( # declaramos el geolocator configurando su precision de localizacion como la mejor posible
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.BEST
        ),
        on_position_change=cambio_ubicacion, # para llamar a un metodo que actualice cuando haya un cambio de posicion
        on_error=lambda e: None # mensaje de error que aparecera en la pantalla
    )

    if not await permitir_ubicacion(geo): # solicitamos el permiso de ubicacion
        return # para salir del programa si no se han concedido los permisos de ubicacion
    
    lat, lon = await posicion_inicial(geo) # obtenemos la posicion actual del usuario
    
    if actualizar_marcador_usuario: 
        actualizar_marcador_usuario(lat, lon) # llamamos a la funcion del mapa para pintar el marcador propio con la posicion inicial

    for miembro in miembros_grupos:
        hilo_listener = Thread(target=listener, args=(miembro,)) # el listener va en un hilo para que pueda estar escuchando y no bloquee el programa
        hilo_listener.start()

    return lat, lon, geo # para poder dibujar la posicion inicial en el mapa y pasar el geo para añadirlo a la pagina desde el mapa en un Stack