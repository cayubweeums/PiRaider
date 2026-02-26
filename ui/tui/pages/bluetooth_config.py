from typing import Any

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Footer, Label, Select, Static, Button

from core.config import get_key, has_key, set_key
from core.radio import grab_all_bluetooth_interfaces


class BluetoothConfigScreen(Screen):
    """Screen to set the active Bluetooth interface (dropdown selection)."""

    BINDINGS = [Binding("q", "pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        interfaces = grab_all_bluetooth_interfaces() or {}
        options = list[str]()

        for controller in interfaces:
            options.append(f"{interfaces[controller]['controller_name']} - Powered: {interfaces[controller]['powered']} - Discoverable: {interfaces[controller]['discoverable']}")


        current = get_key("bluetooth_device") if has_key("bluetooth_device") else None
        initial = current if current in options else (options[0] if options else Select.BLANK)

        yield Static("Bluetooth interface", id="bluetooth_config_title")
        yield Label("Choose interface:")
        if options:
            yield Select.from_values(
                options,
                prompt="Bluetooth interface",
                allow_blank=False,
                value=initial,
                id="bluetooth_interface_select",
            )
        else:
            yield Select(
                [("(no interfaces found)", None)],
                prompt="Bluetooth interface",
                allow_blank=True,
                id="bluetooth_interface_select",
            )
        yield Footer()
        with Horizontal(id="bluetooth_config_actions"):
            yield Button("Save", id="save_bluetooth_config", variant="success")

    # @on(Select.Changed, "#wifi_interface_select")
    # def _on_wifi_select_changed(self, event: Select.Changed) -> None:
    #     if event.value is not None and event.value is not Select.BLANK:
    #         set_key("wifi_device", event.value)

    def action_pop_screen(self) -> None:
        self.app.pop_screen()
        if hasattr(self.app, "refresh_header_from_config"):
            self.app.refresh_header_from_config()
