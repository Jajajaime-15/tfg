import flet as ft
from flet import TextField

def PrimaryButton(text, on_click=None, width=150, disabled=False, loading=False):
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

def delete_Button(on_click=None, width=150, disabled=False, loading=False):
    boton = ft.Button(
        content=ft.Icon(ft.CupertinoIcons.DELETE),
        disabled=disabled or loading,
        on_click=on_click if not disabled and not loading else None,
    )
    return boton

def edit_Button(on_click=None, width=150, disabled=False, loading=False):
    boton = ft.Button(
        content=ft.Icon(ft.Icons.EDIT),
        disabled=disabled or loading,
        on_click=on_click if not disabled and not loading else None,
    )
    return boton

def SecondaryButton(text, on_click=None, width=150, disabled=False, loading=False):
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

def tarjeta_grupos(nombre_grupo, miembros=None, on_click_tarjeta=None, 
                   on_click_anyadir=None, on_click_editar=None, 
                   on_click_eliminar=None, width=400):
    """
    Crea una tarjeta para mostrar información de un grupo.
    """
    
    if miembros is None:
        miembros = []
    
    # Controles de miembros
    miembros_controls = []
    for miembro in miembros:
        miembros_controls.append(
            ft.Text(miembro, size=14, color=ft.Colors.BLACK)
        )
    
    if not miembros_controls:
        miembros_controls.append(
            ft.Text("Sin miembros", size=14, color=ft.Colors.GREY_600)
        )

    # Textfield de nombre 
    nombre_edit_field = TextField(
        value=nombre_grupo,
        width=200,
        text_align=ft.TextAlign.CENTER,
        border_radius=5,
        visible=False
    )    

    # Texto del nombre
    nombre_text = ft.Text(
        nombre_grupo, 
        size=18, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.BLACK,
        visible=True
    )

    # Textfield para nuevo integrante
    integrante_field = ft.TextField(
        label="Nuevo integrante", 
        width=200, 
        color=ft.Colors.BLACK,
        hint_text="Nombre del integrante"
    )

    # Referencia a la tarjeta
    tarjeta = None
    current_nombre = nombre_grupo

    # Botones para edición
    guardar_btn = ft.IconButton(
        icon=ft.Icons.SAVE,
        icon_size=20,
        tooltip="Guardar",
        visible=False,
    )
    
    cancelar_btn = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_size=20,
        tooltip="Cancelar",
        visible=False,
    )

    # Boton editar original
    edit_btn_original = edit_Button(width=30)

    # Botones de edición
    botones_edicion = ft.Row(
        controls=[guardar_btn, cancelar_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        visible=False
    )

    # Contenedor del nombre
    nombre_container = ft.Container(
        content=ft.Stack(
            controls=[nombre_text, nombre_edit_field],
        ),
    )

    # Funciones
    def salir_modo_edicion():
        nonlocal current_nombre
        nombre_edit_field.visible = False
        nombre_text.visible = True
        botones_edicion.visible = False
        edit_btn_original.visible = True
        guardar_btn.visible = False
        cancelar_btn.visible = False
        nombre_edit_field.value = current_nombre
        if tarjeta and tarjeta.page:
            tarjeta.page.update()
    
    def guardar_edicion(e):
        nonlocal current_nombre
        nuevo_nombre = nombre_edit_field.value
        if nuevo_nombre and nuevo_nombre.strip() and nuevo_nombre != current_nombre:
            def despues_de_guardar(exito):
                if exito:
                    current_nombre = nuevo_nombre
                    nombre_text.value = nuevo_nombre
                salir_modo_edicion()
            
            if on_click_editar:
                on_click_editar(current_nombre, nuevo_nombre, despues_de_guardar)
            else:
                salir_modo_edicion()
        else:
            salir_modo_edicion()
    
    def cancelar_edicion(e):
        salir_modo_edicion()
    
    def entrar_modo_edicion(e):
        nombre_text.visible = False
        nombre_edit_field.visible = True
        botones_edicion.visible = True
        edit_btn_original.visible = False
        guardar_btn.visible = True
        cancelar_btn.visible = True
        if tarjeta and tarjeta.page:
            tarjeta.page.update()
            async def do_focus():
                await nombre_edit_field.focus()
            tarjeta.page.run_task(do_focus)
    
    def on_edit_click(e):
        entrar_modo_edicion(e)
    
    def on_plus_click(e):
        if on_click_anyadir:
            on_click_anyadir(current_nombre, integrante_field)
    
    def on_delete_click(e):
        if on_click_eliminar:
            on_click_eliminar(current_nombre)
    
    # Asignar eventos
    edit_btn_original.on_click = on_edit_click
    guardar_btn.on_click = guardar_edicion
    cancelar_btn.on_click = cancelar_edicion

    # Contenido principal
    content = ft.Column(
        controls=[
            nombre_container,
            botones_edicion,
            ft.Text(f"Miembros: {len(miembros)}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            integrante_field,
            ft.Divider(height=10, thickness=1),
            ft.Column(miembros_controls, spacing=5, scroll=ft.ScrollMode.AUTO),
            ft.Container(expand=True),
            ft.Divider(height=10, thickness=1),
            ft.Row(
                controls=[
                    plus_Button(on_click=on_plus_click, width=30),
                    edit_btn_original,
                    delete_Button(on_click=on_delete_click, width=30),
                ],
                alignment=ft.MainAxisAlignment.END, 
            ),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    tarjeta = ft.Container(
        content=content,
        width=width,
        height=450,
        bgcolor=ft.Colors.GREY_200,
        padding=15,
        border_radius=8,
        on_click=on_click_tarjeta,
        ink=True, 
    )
    
    return tarjeta

def IconButton(icon, on_click=None, tooltip="", disabled=False, size=24, icon_color=None, variant="neutral"):
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