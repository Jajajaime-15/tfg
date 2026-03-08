import flet as ft
from views.FletRouter import Router
from db.flet_pyrebase import PyrebaseWrapper

def main(page: ft.Page):

    page.window_height = 500
    page.window_width = 300
    page.scroll = "auto"

    myPyrebase = PyrebaseWrapper(page)
    myRouter = Router(page, myPyrebase)

    page.on_route_change = myRouter.route_change

    page.add(
        myRouter.body
    )

    page.go('/') # para facilitar el cambio de rutas nos sirve go
    myPyrebase.check_token()
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')

