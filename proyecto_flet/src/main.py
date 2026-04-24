import flet as ft
from views.mapa_view import MapaVista
from controllers.mapa_controller import MapaController
from services.gps_service import GPSService

async def main(page: ft.Page):
    service = GPSService(page)
    controller = MapaController(page, service)
    mapa = MapaVista(page, controller)
    controller.vista = mapa
    await controller.iniciar_gps()
    page.add(mapa.vista())

ft.run(main)