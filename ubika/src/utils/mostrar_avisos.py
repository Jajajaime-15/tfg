#import flet as ft

def mostrar_aviso(page, vista, texto, color="red"):
    if vista is not None and hasattr(vista, "mensaje_error"):
        vista.mensaje_error.value = texto
        vista.mensaje_error.color = color
        vista.mensaje_error.visible = True if texto else False
        page.update()