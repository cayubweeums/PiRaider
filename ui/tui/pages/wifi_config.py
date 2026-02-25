from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Footer, Label, Select, Static, Button

from core.config import get_key, has_key, set_key
from core.radio import grab_all_wireless_interfaces


class WifiConfigScreen(Screen):
    """Screen to set the active WiFi interface (dropdown selection)."""

    BINDINGS = [Binding("q", "pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        interfaces = grab_all_wireless_interfaces() or {}
        supported_bands_text = ""
        options = list[str]()

        for interface in interfaces:
            if bool(interfaces[interface]['interface_up']):
                status = "Up"
            else:
                status = "Down"
            if bool(interfaces[interface]['monitor_mode_supported']):
                monitor_mode = "Yes"
            else:
                monitor_mode = "No"
            for band in interfaces[interface]['band_capability']:
                supported_bands_text += f"{interfaces[interface]['band_capability'][band]} GHz, "
            options.append(f"{interfaces[interface]['device_id']} - {status} - mon mode: {monitor_mode} - {supported_bands_text}")

        current = get_key("wifi_device") if has_key("wifi_device") else None
        initial = current if current in options else (options[0] if options else Select.BLANK)

        yield Static("WiFi interface", id="wifi_config_title")
        yield Label("Choose interface:")
        if options:
            yield Select.from_values(
                options,
                prompt="WiFi interface",
                allow_blank=False,
                value=initial,
                id="wifi_interface_select",
            )
        else:
            yield Select(
                [("(no interfaces found)", None)],
                prompt="WiFi interface",
                allow_blank=True,
                id="wifi_interface_select",
            )
        yield Footer()
        with Horizontal(id="wifi_config_actions"):
            yield Button("Save", id="save_wifi_config", variant="success")

    # @on(Select.Changed, "#wifi_interface_select")
    # def _on_wifi_select_changed(self, event: Select.Changed) -> None:
    #     if event.value is not None and event.value is not Select.BLANK:
    #         set_key("wifi_device", event.value)

    def action_pop_screen(self) -> None:
        self.app.pop_screen()
        if hasattr(self.app, "refresh_header_from_config"):
            self.app.refresh_header_from_config()
