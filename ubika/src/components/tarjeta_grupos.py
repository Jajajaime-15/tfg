import flet as ft 
from components.boton_acciones import BotonAcciones

class TarjetaGrupo(ft.Container):
    def __init__(self, nombre_grupo, id_usuario, id_admin_grupo, miembros=None, emails=None, on_agregar=None, on_editar=None, on_eliminar=None, 
                on_abandonar=None, on_eliminar_integrante=None, on_click_tarjeta=None, width=350):
        super().__init__()
        # guardamos los datos
        self.current_nombre = nombre_grupo
        self.id_usuario = id_usuario
        self.id_admin_grupo = id_admin_grupo
        self.es_admin = (id_usuario == id_admin_grupo) # obtenemos el rol del usuario en el grupo

        self.miembros = miembros or []
        self.emails = emails or []
        self.modo_edicion = False

        self.on_agregar = on_agregar
        self.on_editar = on_editar
        self.on_eliminar = on_eliminar
        self.on_abandonar = on_abandonar
        self.on_eliminar_integrante = on_eliminar_integrante
        self.on_click = on_click_tarjeta # se le asigna el evento al Containe 
        self.ink = True # ponemos un efecto visual que se vea al pulsar

        # definimos los componentes uno a uno
        self.columna_miembros = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO) # columna de los miembros
        
        self.grupo = ft.Text(nombre_grupo, size=20, color="black", weight="bold") # nombre del grupo

        self.editar_nombre_grupo = ft.TextField(value=nombre_grupo, width=150, height=40, color="black", visible=False, border=ft.InputBorder.UNDERLINE, text_size=16) # campo editar nombre de grupo
        self.integrante = ft.TextField(width=150, height=40, color="black", hint_text="Email del integrante", visible=False, border=ft.InputBorder.UNDERLINE, text_size=16) # campo agregar miembro

        self.btn_guardar = BotonAcciones(ft.Icons.SAVE,  accion=self.guardar_edicion, tooltip="Guardar cambios", visible=False)
        self.btn_cancelar = BotonAcciones(ft.Icons.CLOSE, accion=self.cancelar_edicion, tooltip="Cancelar", color_icono="red", visible=False)

        self.btn_editar = BotonAcciones(ft.Icons.EDIT, accion=self.entrar_modo_edicion,tooltip="Editar grupo")
        self.btn_agregar = BotonAcciones(ft.Icons.ADD, accion=self.agregar, tooltip="Agregar miembro")
        self.btn_agregar.visible = False
        self.btn_eliminar_grupo = BotonAcciones(ft.Icons.DELETE, accion=self.eliminar, tooltip="Eliminar grupo")
        self.btn_eliminar_grupo.visible = False
        self.btn_salir = BotonAcciones(ft.Icons.LOGOUT_ROUNDED, accion=self.abandonar, tooltip="Salir del grupo")

        self.width = width
        self.bgcolor = ft.Colors.with_opacity(0.6, "#F0F4F8")
        self.padding = 30
        self.border_radius = 15
        self.shadow = ft.BoxShadow(spread_radius=-1, blur_radius=8, color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK), offset=ft.Offset(4, 4))
        self.border = ft.border.all(0.5, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))
        self.content = self.crear_vista() # creamos la vista
        self.actualizar_controles_miembros() # actualizamos

    def crear_vista(self):
        fila_admin = ft.Row( # botones que se van a mostrar abajo si es admin del grupo
            controls=[self.btn_editar, self.btn_eliminar_grupo,self.btn_cancelar],
            alignment=ft.MainAxisAlignment.END,
        )

        fila_miembro = ft.Row( # botones que se van a mostrar abajo si es miembro del grupo
            controls=[self.btn_salir],
            alignment=ft.MainAxisAlignment.END,
        )

        return ft.Column(
            controls=[
                ft.Row([ # fila con el nombre del grupo
                    ft.Icon(ft.Icons.PEOPLE, color="#1A6AFE", size=24),
                    self.grupo, self.editar_nombre_grupo, self.btn_guardar
                ], alignment=ft.MainAxisAlignment.CENTER),

                ft.Row([ # fila con el total de miembros
                    ft.Text(f"Miembros: {len(self.miembros)}", size=18, color="black", weight="bold")
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Row([self.integrante, self.btn_agregar], alignment=ft.MainAxisAlignment.CENTER), # fila agregar nuevo miembro

                ft.Divider(height=10),
                ft.Container(content=self.columna_miembros, height=200), # contenedor con la list ade miembros
                ft.Divider(height=10),
                
                fila_admin if self.es_admin else fila_miembro # se comprueba que rol tiene el usuario en el grupo
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

    def actualizar_controles_miembros(self):
        self.columna_miembros.controls.clear()

        for i, miembro in enumerate(self.miembros):
            email_m = self.emails[i] if i < len(self.emails) else ""
            
            contenido = ft.Column(
                controls=[ft.Text(miembro, size=16, color="black", weight="w500"),
                        ], spacing=0, tight=True, expand=True
            )
            
            if self.modo_edicion and email_m:
                contenido.controls.append(ft.Text(email_m, size=12, color="blue700"))

            fila = ft.Row([
                ft.Icon(ft.Icons.PERSON, color="#1A6AFE", size=20),
                contenido,
            ],alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.VerticalAlignment.CENTER)

            # comprobamos que es admin y está en modo edicion para eliminar miembro
            if self.es_admin and self.modo_edicion and email_m != self.id_usuario: # comprobamos que el email es diferente al del usuario
                fila.controls.append(
                    BotonAcciones(
                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE, 
                        accion=lambda e, em=email_m: self.borrar_integrante(e, em),
                        tooltip="Eliminar del grupo",
                        color_icono="red", 
                        size=18,
                    )
                )

            self.columna_miembros.controls.append(
                ft.Container(content=fila, padding=ft.padding.symmetric(vertical=2))
            )

    def entrar_modo_edicion(self, e):
        self.modo_edicion = True
        self.alternar_visibilidad(True)
        self.actualizar_controles_miembros()

    def salir_modo_edicion(self):
        self.modo_edicion = False
        self.alternar_visibilidad(False)
        self.editar_nombre_grupo.value = self.current_nombre
        self.actualizar_controles_miembros()

    def alternar_visibilidad(self, editando):
        self.grupo.visible = not editando
        self.editar_nombre_grupo.visible = editando
        self.btn_editar.visible = not editando
        self.btn_guardar.visible = editando
        self.btn_cancelar.visible = editando
        self.btn_eliminar_grupo.visible = editando
        self.btn_agregar.visible = editando
        self.integrante.visible = editando

        self.actualizar_controles_miembros()
        self.update()

    def guardar_edicion(self, e):
        nuevo = self.editar_nombre_grupo.value
        if nuevo and nuevo.strip() and nuevo != self.current_nombre:
            if self.on_editar:
                self.on_editar(self.current_nombre, nuevo, self.finalizar_guardado)
            else:
                self.finalizar_guardado(True)
        else:
            self.salir_modo_edicion()

    def finalizar_guardado(self, exito):
        if exito:
            self.current_nombre = self.editar_nombre_grupo.value
            self.grupo.value = self.current_nombre
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

    def abandonar(self, e):
        if self.on_abandonar:
            self.on_abandonar(self.current_nombre)