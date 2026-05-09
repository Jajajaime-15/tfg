import flet as ft

def plus_Button(on_click=None, width=150, disabled=False, loading=False):
    boton = ft.Button(
        content=ft.Icon(ft.Icons.ADD),
        disabled=disabled or loading,
        on_click=on_click if not disabled and not loading else None,
    )
    return boton