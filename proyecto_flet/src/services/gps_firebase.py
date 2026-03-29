import flet as ft # para flet
import pyrebase # para firebase
import flet_geolocator as ftg # para la geolocalizacion
import flet_map as ftm # para el mapa
from db.config import config_keys # las claves que tenemos en el .env
from threading import Thread

firebase = pyrebase.initialize_app(config_keys) # iniciamos firebase
db = firebase.database() # instanciamos la base de datos y la autenticacion
auth = firebase.auth()


async def gps(page: ft.Page):
    print("Firebase conectado")
    page.add(ft.Text("Firebase conectado"))

    def cambio_ubicacion(cambio: ftg.GeolocatorPositionChangeEvent):
        loc = {
            "latitud" : cambio.position.latitude,
            "longitud" : cambio.position.longitude,
            "timestamp" : str(cambio.position.timestamp)
        }
        db.child("ubicaciones").child("grupo_01").child("jaime").set(loc)
        page.add(ft.Text(f"Cambio ubicacion OK: {cambio.position.latitude} {cambio.position.longitude} {cambio.position.timestamp}"))

    geo = ftg.Geolocator( # declaramos el geolocator configurando su precision de localizacion como la mejor posible
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.BEST
        ),
        on_position_change=cambio_ubicacion, # para llamar a un metodo que actualice cuando haya un cambio de posicion
        on_error=lambda e: None # mensaje de error que aparecera en la pantalla
    )

    permiso_localizacion = await geo.get_permission_status() # comprobamos si esta habilitado el permiso de localizacion en el dispositivo
    if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE): # en caso de NO estar habilitado
        await geo.request_permission() # solicitamos permiso
        permiso_localizacion = await geo.get_permission_status() # comprobamos de nuevo
        if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE):
            page.add(ft.Text(f"Permisos de localización no habilitados"))
            return # avisamos de que no han sido habilitados y hacemos que no se siga ejecutando la funcion
    
    localizacion = await geo.get_current_position() # obtenemos la posicion actual del dispositivo
    page.add(ft.Text(f"Localizacion: {localizacion}"))
    page.add(ft.Text(f"Latitud: {localizacion.latitude}"))
    page.add(ft.Text(f"Longitud: {localizacion.longitude}"))
    page.add(ft.Text(f"Altitud: {localizacion.altitude}"))
    page.add(ft.Text(f"Velocidad: {localizacion.speed}"))
    page.add(ft.Text(f"Fecha: {localizacion.timestamp}"))

    loc = {
        "latitud" : localizacion.latitude,
        "longitud" : localizacion.longitude,
        "timestamp" : str(localizacion.timestamp) # el timestamp no es algo valido en json asi que hay que convertirlo a string
    }
    try:
        db.child("ubicaciones").child("grupo_01").child("jaime").set(loc) # para escribir los valores debemos marcar el nivel dentro de los json con los 'child' y 'set'
        page.add(ft.Text(f"Escritura OK"))
    except Exception as e:
        page.add(ft.Text(f"Error escritura Firebase: {e}"))
    


    def cambio_ubicacion_amigo(ubicacion_amigo): # funcion callback para usar el cambio de la ubicacion
        page.add(ft.Text(f"{ubicacion_amigo}")) # por ahora solo lo escribimos en pantalla
    
    def listener(): # listener para recibir cada vez que haya un cambio en la ubicacion de alguien
        db.child("ubicaciones").child("grupo_01").stream(cambio_ubicacion_amigo) # el stream hace que escuchemos constantemente esta parte de realtime por si hay cambios y llamamos al callback

    hilo_listener = Thread(target=listener) # el listener va en un hilo para que pueda estar escuchando y no bloquee el programa
    hilo_listener.start()

    page.add(geo)