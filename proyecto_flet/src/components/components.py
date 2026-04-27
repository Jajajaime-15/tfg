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

def plus_Button(on_click=None, width=150, disabled=False, loading=False):
    
    boton = ft.Button(
        content=ft.Icon(ft.CupertinoIcons.PLUS_CIRCLE_FILL),
        disabled=disabled or loading,
        on_click=on_click if not disabled and not loading else None,
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

def tarjeta_grupos(nombre_grupo, miembros=None, on_click_tarjeta=None, on_click_anyadir=None, width=400):
    """
    Crea una tarjeta para mostrar información de un grupo.
    
    Parámetros:
        nombre_grupo: Nombre del grupo (string)
        miembros: Lista de miembros del grupo (lista de strings)
        on_click: Función a ejecutar al hacer clic
        width: Ancho de la tarjeta
        height: Alto de la tarjeta
    """
    
    if miembros is None:
        miembros = []
    
    # lista de textos para los miembros
    miembros_controls = []
    for miembro in miembros:
        miembros_controls.append(
            ft.Text(miembro, size=14, color=ft.Colors.BLACK)
        )
    
    # Si no hay miembros, mostrar un mensaje
    if not miembros_controls:
        miembros_controls.append(
            ft.Text("Sin miembros", size=14, color=ft.Colors.GREY_600)
        )
    
    # Crear el TextField para nuevo integrante
    integrante_field = ft.TextField(
        label="Nuevo integrante", 
        width=200, 
        color=ft.Colors.BLACK,
        hint_text="Nombre del integrante"
    )

    # Función para manejar el click en el botón anyadir
    def on_plus_click(e):
        if on_click_anyadir:
            # Llamar a on_click_anyadir con el nombre del grupo y el integrante
            on_click_anyadir(nombre_grupo, integrante_field)

    content = ft.Column(
        controls=[
            ft.Row(
                ft.Text(nombre_grupo, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                alignment=ft.MainAxisAlignment.CENTER
                ),  # Espacio superior,
            ft.Text(f"Miembros: {len(miembros)}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            integrante_field,
            ft.Divider(height=10, thickness=1),
            ft.Column(miembros_controls, spacing=5, scroll=ft.ScrollMode.AUTO),
            ft.Container(expand=True),
            ft.Divider(height=10, thickness=1),
            ft.Row(
            [plus_Button(on_click=on_plus_click, width=30)],
            alignment=ft.MainAxisAlignment.END, 
        ),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    
    tarjeta = ft.Container(
        content=content,
        width=width,
        height=400,
        bgcolor=ft.Colors.GREY_200,
        padding=15,
        border_radius=8,
        on_click=on_click_tarjeta,
        ink=True, 
    )
    
    return tarjeta

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