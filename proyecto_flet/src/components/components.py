import flet as ft


def PrimaryButton(text, on_click=None, width=150, disabled=False, loading=False):
    
    #Disabled =  True:No permite que el botón sea interactivo, esto puede ser valido para evitar acciones no deseadas o para indicar que un campo está sin rellenar
    #Loading = True: Muestra un indicador de carga junto al texto del botón, y el botón se desactiva mientras se muestra el indicador de carga.
    
    if loading:
        content = ft.Row(
            [
                ft.ProgressRing(
                    width=20,
                    height=20,
                    stroke_width=2,
                    color=ft.Colors.BLACK,
                ),
                ft.Text(
                    text,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    else:
        content = ft.Text(
            text,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
        )
    
    
    boton = ft.Button(
        content=content,
        width=width,
        disabled=disabled or loading,  
        on_click=on_click if not disabled and not loading else None,  
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            color={
                ft.ControlState.HOVERED: ft.Colors.BLACK,
                ft.ControlState.FOCUSED: ft.Colors.BLACK,
                ft.ControlState.DEFAULT: ft.Colors.BLACK,
            },
            bgcolor={
                ft.ControlState.HOVERED: ft.Colors.GREY_300,
                ft.ControlState.FOCUSED: ft.Colors.GREY_300,
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
            },
        ),
    )
    
    return boton

def SecondaryButton(text, on_click=None, width=150, disabled=False, loading=False):
    
    # Este segundo boton se utilizará principalmente para acciones secundarias, como "Registrarse", "Cancelar", etc.
    
    if loading:
        content = ft.Row(
            [
                ft.ProgressRing(
                    width=20,
                    height=20,
                    stroke_width=2,
                    color=ft.Colors.BLACK,
                ),
                ft.Text(
                    text,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    else:
        content = ft.Text(
            text,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
        )
    
    
    boton = ft.Button(
        content=content,
        width=width,
        disabled=disabled or loading,  
        on_click=on_click if not disabled and not loading else None,  
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            color={
                ft.ControlState.HOVERED: ft.Colors.GREY_50,
                ft.ControlState.FOCUSED: ft.Colors.GREY_50,
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            bgcolor={
                ft.ControlState.HOVERED: ft.Colors.GREY_400,
                ft.ControlState.FOCUSED: ft.Colors.GREY_400,
                ft.ControlState.DEFAULT: ft.Colors.GREY_200,
            },
        ),
    )
    
    return boton

def IconButton(
    icon, 
    on_click=None, 
    tooltip="", 
    disabled=False, 
    size=24, 
    icon_color=None,
    variant="neutral"  # 'neutral', 'positive', 'danger'
):
    """
    
    Parametros:

        icon: Icono a mostrar (puede ser un ícono de Flet o una imagen personalizada)
        size: Tamaño del ícono en píxeles
        icon_color: Color específico (sobrescribe a variant)
        variant: 'neutral' (gris), 'positive' (azul), 'negative' (rojo)
    
    """
    
    if icon_color is None:
        if variant == "neutral":
            normal_color = ft.Colors.GREY_700
            hover_color = ft.Colors.GREY_900
        elif variant == "positive":
            normal_color = ft.Colors.BLUE_600
            hover_color = ft.Colors.BLUE_800
        elif variant == "negative":
            normal_color = ft.Colors.RED_500
            hover_color = ft.Colors.RED_700
        else:
            normal_color = ft.Colors.GREY_700
            hover_color = ft.Colors.GREY_900
    else:
        normal_color = icon_color
        hover_color = icon_color
    
    
    boton = ft.IconButton(
        icon=icon,
        icon_size=size,
        tooltip=tooltip,
        disabled=disabled,
        on_click=on_click if not disabled else None,
        icon_color={
            ft.ControlState.HOVERED: hover_color,
            ft.ControlState.FOCUSED: hover_color,
            ft.ControlState.DEFAULT: normal_color,
            ft.ControlState.DISABLED: ft.Colors.GREY_400,
        },
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, normal_color),
                ft.ControlState.FOCUSED: ft.Colors.with_opacity(0.1, normal_color),
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
        ),
    )
    
    return boton


    
