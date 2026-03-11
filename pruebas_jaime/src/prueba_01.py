import flet as ft


def main(page: ft.Page):
    counter = ft.Text("1", size=50, data=0)

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)

    def minus_click(e):
        counter.data -= 1
        counter.value = str(counter.data)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )
    restar = ft.IconButton (
        icon=ft.Icons.REMOVE, on_click=minus_click
    )
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Row(
                [
                    restar,
                    counter
                ],
                alignment=ft.Alignment.CENTER,
            ),
        )
    )


ft.run(main)
