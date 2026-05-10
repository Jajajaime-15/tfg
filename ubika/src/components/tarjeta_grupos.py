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
        self.btn_agregar = BotonAgregar(accion=self.agregar, ancho=40, deshabilitado=False)
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
                    alignment=ft.MainAxisAlignment.CENTER),
                
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
                        BotonEliminar(accion=self.eliminar, ancho=40),
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

    def agregar(self, e):
        if self.on_agregar:
            self.on_agregar(self.current_nombre, self.integrante)

    def eliminar(self, e):
        if self.on_eliminar:
            self.on_eliminar(self.current_nombre)

    def borrar_integrante(self, e, email):
        if self.on_eliminar_integrante:
            self.on_eliminar_integrante(e, self.current_nombre, email)
            self.salir_modo_edicion()