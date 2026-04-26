import requests

# funcion para realizar la llamada a la api de nominatim con los datos de la localizacion de un usuario y obtener una direccion entendible para cualquiera
def obtener_direccion_legible(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json" # la llamada a la api recibe los parametros de la direccion

    headers = { 
        'User-Agent': 'Ubika/1.0' # se requiere al menos un user agent para llamar a esta api
    }

    try:
        response = requests.get(url=url, headers=headers)
        respuesta_json = response.json() # convertimos la respuesta en json
        ubicacion = respuesta_json["display_name"] # obtenemos la direccion
    except Exception as e:
        ubicacion = "Ubicación no disponible"
        print(f"Error al intentar obtener la ubicacion: {e}")

    return ubicacion