import flet as ft
import flet_map as ftm


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ftm.Map(
                expand=True,
                initial_center=ftm.MapLatitudeLongitude(40.4168, -3.7038),
                initial_zoom=10,
                on_init=lambda e: print("Map initialized"),
                layers=[
                    ftm.TileLayer(
                        url_template="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png",
                        user_agent_package_name="com.tfg.tracking",
                        on_image_error=lambda e: print(f"TileLayer Error: {e.data}"),
                    ),
                ],
            ),
        )
    )


ft.run(main)
