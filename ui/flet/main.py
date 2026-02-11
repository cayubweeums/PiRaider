import asyncio

import flet as ft

def flet_main(web: bool = False):
    if not web:
        ft.run(main)
    else:
        ft.run(main, view=ft.AppView.WEB_BROWSER, port=8080)

def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change():
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(
                        title=ft.Text("The App"), bgcolor=ft.Colors.SURFACE_BRIGHT
                    ),
                    ft.Button(
                        "Visit Store",
                        on_click=lambda: asyncio.create_task(page.push_route("/store")),
                    ),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    route="/store",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Store"), bgcolor=ft.Colors.SURFACE_BRIGHT
                        ),
                        ft.Button(
                            "Go Home",
                            on_click=lambda: asyncio.create_task(page.push_route("/")),
                        ),
                    ],
                )
            )
        page.update()

    async def view_pop(e):
        if e.view is not None:
            print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()