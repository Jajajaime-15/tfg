import flet as ft # para flet
import pyrebase # para firebase
import flet_geolocator as ftg # para la geolocalizacion
import flet_map as ftm # para el mapa
from db.config import config_keys # las claves que tenemos en el .env

firebase = pyrebase.initialize_app(config_keys) # iniciamos firebase
db = firebase.database() # instanciamos la base de datos y la autenticacion
auth = firebase.auth()


async def main(page: ft.Page):
    print("Firebase conectado")
    page.add(ft.Text("Firebase conectado"))
    geo = ftg.Geolocator( # declaramos el geolocator configurando su precision de localizacion como la mejor posible
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.BEST
        ),
        on_position_change=None, # para llamar a un metodo que actualice cuando haya un cambio de posicion
        on_error=None # mensaje de error que aparecera en la pantalla
    )

    permiso_localizacion = await geo.get_permission_status() # comprobamos si esta habilitado el permiso de localizacion en el dispositivo
    if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE): # en caso de NO estar habilitado
        await geo.request_permission() # solicitamos permiso
        permiso_localizacion = await geo.get_permission_status() # comprobamos de nuevo
        if (permiso_localizacion != ftg.GeolocatorPermissionStatus.ALWAYS) and (permiso_localizacion != ftg.GeolocatorPermissionStatus.WHILE_IN_USE):
            page.add(ft.Text(f"Permisos de localización no habilitados"))
            return # avisamos de nuevo y hacemos que no se siga ejecutando la funcion

ft.run(main)