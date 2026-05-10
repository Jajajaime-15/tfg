'''import flet as ft
from flet import TextField
from ubika.src.components.boton_agregar import plus_Button
from ubika.src.components.boton_eliminar import delete_Button
from ubika.src.components.boton_editar import edit_Button

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
        color=ft.Colors.BLACK,
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

'''

import flet as ft 
from components.boton_agregar import BotonAgregar
from components.boton_eliminar import BotonEliminar
from components.boton_editar import BotonEditar

class TarjetaGrupo(ft.Container):
    def __init__(self, nombre_grupo, miembros=None, emails=None, on_agregar=None, on_editar=None, on_eliminar=None, 
                on_eliminar_integrante=None, on_click_tarjeta=None, width=400):
        super().__init__()
        # guardamos los datos
        self.current_nombre = nombre_grupo
        self.miembros = miembros or []
        self.emails = emails or []
        self.modo_edicion = False
        self.on_agregar = on_agregar
        self.on_editar = on_editar
        self.on_eliminar = on_eliminar
        self.on_eliminar_integrante = on_eliminar_integrante
        self.on_click = on_click_tarjeta # se le asigna el evento al Containe 
        self.ink = True # ponemos un efecto visual que se vea al pulsar

        # definimos los componentes uno a uno
        self.columna_miembros = ft.Column(spacing=5)
        self.nombre_text = ft.Text(nombre_grupo, size=20, weight=ft.FontWeight.BOLD, color="black") 
        self.grupo = ft.TextField(value=nombre_grupo, color="black", width=200, text_align=ft.TextAlign.CENTER, visible=False)
        self.integrante = ft.TextField(label="Nuevo integrante", width=200, color=ft.Colors.BLACK, hint_text="Email del integrante", visible=False)
        self.btn_guardar = ft.IconButton(ft.Icons.SAVE, visible=False, on_click=self.guardar_edicion)
        self.btn_cancelar = ft.IconButton(ft.Icons.CLOSE, visible=False, on_click=self.cancelar_edicion)
        self.btn_editar = BotonEditar(accion=self.entrar_modo_edicion, ancho=40)
        self.btn_agregar = BotonAgregar(accion=self.on_plus_click, ancho=40, deshabilitado=False)
        self.btn_agregar.visible = False
        
        self.width = width
        self.bgcolor = ft.Colors.GREY_100
        self.padding = 15
        self.border_radius = 10
        
        self.content = self.crear_vista() # creamos la vista
        self.actualizar_controles_miembros() # actualizamos

    def crear_vista(self):
        return ft.Column(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.PEOPLE, color="#1A6AFE", size=22),
                    ft.Stack([self.nombre_text, self.grupo]),
                ], alignment=ft.MainAxisAlignment.CENTER),

                ft.Row([self.btn_guardar, self.btn_cancelar], 
                    alignment=ft.MainAxisAlignment.CENTER, visible=False),
                
                ft.Row([
                    ft.Text(f"Miembros: {len(self.miembros)}", size=18, weight="bold", color="black")
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                self.integrante,
                ft.Divider(height=10),
                self.columna_miembros,
                ft.Container(expand=True),
                ft.Divider(height=10),
                
                ft.Row(
                    controls=[
                        self.btn_agregar,
                        self.btn_editar,
                        BotonEliminar(accion=self.on_delete_click, ancho=40),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=10,
        )

    def actualizar_controles_miembros(self):
        self.columna_miembros.controls.clear()
        if not self.miembros:
            self.columna_miembros.controls.append(
                ft.Text("Sin miembros todavía", size=14, color=ft.Colors.GREY_600)
            )
        else:
            for i, miembro in enumerate(self.miembros):
                email_m = self.emails[i] if i < len(self.emails) else ""
                
                fila = ft.Row([
                    ft.Icon(ft.Icons.PERSON, color="#1A6AFE", size=20),
                    ft.Text(miembro, size=16, color="black", expand=True),
                ])

                if self.modo_edicion and self.on_eliminar_integrante:
                    fila.controls.append(
                        ft.IconButton(
                            icon=ft.Icons.CLOSE, icon_color="red", icon_size=16,
                            on_click=lambda e, em=email_m: self.borrar_integrante(e, em)
                        )
                    )

                self.columna_miembros.controls.append(
                    ft.Container(content=fila, bgcolor=ft.Colors.GREY_200, 
                                padding=8, border_radius=8)
                )

    def entrar_modo_edicion(self, e):
        self.modo_edicion = True
        self.alternar_visibilidad(True)
        self.actualizar_controles_miembros()
        self.update()

    def salir_modo_edicion(self):
        self.modo_edicion = False
        self.alternar_visibilidad(False)
        self.grupo.value = self.current_nombre
        self.actualizar_controles_miembros()
        self.update()

    def alternar_visibilidad(self, editando):
        self.nombre_text.visible = not editando
        self.grupo.visible = editando
        self.btn_editar.visible = not editando
        self.btn_guardar.visible = editando
        self.btn_cancelar.visible = editando
        self.btn_agregar.visible = editando
        self.integrante.visible = editando

    def guardar_edicion(self, e):
        nuevo = self.grupo.value
        if nuevo and nuevo.strip() and nuevo != self.current_nombre:
            if self.on_editar:
                self.on_editar(self.current_nombre, nuevo, self.finalizar_guardado)
            else:
                self.finalizar_guardado(True)
        else:
            self.salir_modo_edicion()

    def finalizar_guardado(self, exito):
        if exito:
            self.current_nombre = self.grupo.value
            self.nombre_text.value = self.current_nombre
        self.salir_modo_edicion()

    def cancelar_edicion(self, e):
        self.salir_modo_edicion()

    def on_plus_click(self, e):
        if self.on_agregar:
            self.on_agregar(self.current_nombre, self.integrante)

    def on_delete_click(self, e):
        if self.on_eliminar:
            self.on_eliminar(self.current_nombre)

    def borrar_integrante(self, e, email):
        if self.on_eliminar_integrante:
            self.on_eliminar_integrante(e, self.current_nombre, email)
            self.salir_modo_edicion()