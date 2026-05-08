import flet as ft
from flet import TextField



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


def tarjeta_grupos(nombre_grupo, miembros=None, 
                   emails = None, on_click_tarjeta=None, 
                   on_click_anyadir=None, on_click_editar=None, 
                   on_click_eliminar=None, on_click_eliminar_integrante=None, width=400):
    
    if miembros is None:
        miembros = []

    if emails is None:
        emails = []


    # Variable para controlar modo edición
    modo_edicion = False
    
    # Controles de miembros
    columna_miembros = ft.Column(spacing=5)
    
    def actualizar_controles_miembros():
        columna_miembros.controls.clear()
        for i, miembro in enumerate(miembros):
            if modo_edicion and on_click_eliminar_integrante:
                email_miembro = emails[i] if i < len(emails) else "Email no disponible"
                columna_miembros.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, color="#1A6AFE", size=20),
                            ft.Text(miembro, size=16, color=ft.Colors.BLACK, expand=True),
                            ft.Text(email_miembro, size=12, color=ft.Colors.BLACK),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_size=16,
                                icon_color="red",
                                tooltip="Eliminar integrante",
                                on_click=lambda e, email=email_miembro: (on_click_eliminar_integrante(e, nombre_grupo, email), salir_modo_edicion()),
                            ),
                        ]),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=10,
                        padding=10,
                    )
                )
            else:
                columna_miembros.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, color="#1A6AFE", size=20),
                            ft.Text(miembro, size=16, color=ft.Colors.BLACK),
                        ]),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=10,
                        padding=10,
                    )
                )
    
    actualizar_controles_miembros()
    
    if not miembros:
        columna_miembros.controls.append(
            ft.Text("Este grupo todavia no tiene miembros", size=18, color=ft.Colors.GREY_600)
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
        size=20, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.BLACK,
        visible=True
    )

    # Textfield para nuevo integrante
    integrante_field = ft.TextField(
        label="Nuevo integrante", 
        width=200, 
        color=ft.Colors.BLACK,
        hint_text="Email del integrante",
        visible=False
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

    # Botón plus para añadir integrante
    plus_btn = plus_Button(width=30)
    plus_btn.visible = False

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
        nonlocal current_nombre, modo_edicion
        modo_edicion = False
        nombre_edit_field.visible = False
        nombre_text.visible = True
        botones_edicion.visible = False
        edit_btn_original.visible = True
        guardar_btn.visible = False
        cancelar_btn.visible = False
        plus_btn.visible = False
        integrante_field.visible = False
        nombre_edit_field.value = current_nombre
        actualizar_controles_miembros()
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
        nonlocal modo_edicion
        modo_edicion = True
        nombre_text.visible = False
        nombre_edit_field.visible = True
        botones_edicion.visible = True
        edit_btn_original.visible = False
        guardar_btn.visible = True
        cancelar_btn.visible = True
        plus_btn.visible = True
        integrante_field.visible = True
        actualizar_controles_miembros()
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
    plus_btn.on_click = on_plus_click

    # Contenido principal
    content = ft.Column(
        controls=[
            ft.Row([
                ft.Icon(ft.Icons.PEOPLE, color="#1A6AFE", size=22),
                nombre_container
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,),
            botones_edicion,
            ft.Row([
                ft.Text(f"Miembros: {len(miembros)}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,),
            integrante_field,
            ft.Divider(height=10, thickness=1),
            columna_miembros,
            ft.Container(expand=True),
            ft.Divider(height=10, thickness=1),
            ft.Row(
                controls=[
                    plus_btn,
                    edit_btn_original,
                    delete_Button(on_click=on_delete_click, width=30),
                ],
                alignment=ft.MainAxisAlignment.END, 
            ),
        ],
        spacing=10,
    )
    
    tarjeta = ft.Container(
        content=content,
        width=width,
        height=450,
        bgcolor=ft.Colors.GREY_100,
        padding=15,
        border_radius=8,
        on_click=on_click_tarjeta,
        ink=True, 
    )
    
    return tarjeta

