from datetime import datetime, timezone, timedelta

# utilidad para poder formatear el timestamp que almacenamos en firebase
def formatear_timestamp(timestamp):
    try:
        fecha = datetime.fromisoformat(timestamp) # pasamos el string del timestamp a un objeto datetime
        zona_horaria_espanya = timezone(timedelta(hours=2)) # la zona horaria de españa en verano, habra que cambiarlo en invierno
        formato_espanya = fecha.astimezone(zona_horaria_espanya) # transformamos el datetime en el formato de españa
        return formato_espanya.strftime("%d/%m/%Y, %H:%M:%S") # lo mostramos como estamos acostumbrados en españa
    except Exception as e:
        print(f"Excepcion al formatear el timestamp: {e}")
        return timestamp