import asyncio

import flet as ft

from .pages.home import home_page
from .pages.devices import devices_page
from .pages.settings_wifi import Wifi_Settings_Content
from .pages.settings_bluetooth import Bluetooth_Settings_Content

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
                    controls=Wifi_Settings_Content(page).get_content()
                )
            )
        if page.route == "/bluetooth":
            page.views.append(
                ft.View(
                    route="/bluetooth",
                    controls=Bluetooth_Settings_Content(page).get_content()
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
                    controls=Wifi_Settings_Content(page).get_content()
                )
            )
        if page.route == "/settings_bluetooth":
            page.views.append(
                ft.View(
                    route="/settings_bluetooth",
                    controls=Bluetooth_Settings_Content(page).get_content()
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