import asyncio

import flet as ft

from .pages.home import home_page
from .pages.wifi import wifi_page
from .pages.bluetooth import bluetooth_page
from .pages.devices import devices_page
from .pages.settings_wifi import settings_wifi_page

'''
# Flet main entrypoint
'''
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
                controls=home_page(page),
            )
        )
        if page.route == "/wifi":
            page.views.append(
                ft.View(
                    route="/wifi",
                    controls=wifi_page(page)
                )
            )
        if page.route == "/bluetooth":
            page.views.append(
                ft.View(
                    route="/bluetooth",
                    controls=bluetooth_page(page)
                )
            )
        if page.route == "/devices":
            page.views.append(
                ft.View(
                    route="/devices",
                    controls=devices_page(page)
                )
            )
        if page.route == "/settings_wifi":
            page.views.append(
                ft.View(
                    route="/settings_wifi",
                    controls=settings_wifi_page(page)
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