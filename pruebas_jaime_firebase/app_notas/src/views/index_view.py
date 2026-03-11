import flet as ft

def IndexView(page, myPyrebase=None):
    title = "Flet + Pyrebase"

    async def on_load():
        result = await myPyrebase.check_token()
        if result == "Success":
            page.go('/dashboard')

    def handle_sign_in_error():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Incorrect Info. Please Try Again.", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED,
            open=True
        )

    def handle_sign_in(e):
        try:
            myPyrebase.sign_in(email.value, password.value)
            password.value = ""
            page.go("/dashboard")
        except:
            handle_sign_in_error()
            page.update()

    def handle_register(e):
        page.go('/register')
        
    def handle_google(e):
        google_button.scale = 0.9

    def handle_google_hover(e):
        pass

    banner = ft.Image(src='banner.jpg', width=250, border_radius=5, fit="cover")
    welcome_text = ft.Text("Welcome", size=26, bottom=10, right=10, color=ft.Colors.WHITE_70)
    email = ft.TextField(label="Email", width=250)
    password = ft.TextField(label="Password", width=250, password=True)

    sign_in_button = ft.TextButton("Sign In", on_click=handle_sign_in)
    register_button = ft.TextButton("Register", on_click=handle_register)

    google_button = ft.Container(ft.Image(src="btn_google_dark.png", width=250), on_click=handle_google, on_hover=handle_google_hover)
    
    myPage = ft.Column(
        [
            ft.Container(
                ft.Stack(
                [
                    banner,
                    welcome_text
                    ]
            ), alignment=ft.Alignment(0, 0)
            ),
            ft.Row(
                [email],
                alignment=ft.MainAxisAlignment.CENTER
                ),
            ft.Row(
                [password],
                alignment=ft.MainAxisAlignment.CENTER
                ),
            ft.Row(
                [register_button, sign_in_button],
            alignment=ft.MainAxisAlignment.CENTER),
        ]
            )
    
    return {
        "view": myPage,
        "title": title,
        "load": on_load
        }