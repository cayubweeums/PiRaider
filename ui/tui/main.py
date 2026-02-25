from textual.app import App, ComposeResult
from textual.widgets import Footer, Button, RadioButton
from textual.containers import HorizontalGroup

from core.config import has_key
from ui.tui.widgets.custom_header import CustomHeader
from ui.tui.pages.wifi_config import WifiConfigScreen
from ui.tui.pages.bluetooth_config import BluetoothConfigScreen


class BucketsGroup(HorizontalGroup):
    """A group of buckets."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a buckets group."""
        yield Button("WiFi", id="wifi")
        yield Button("Bluetooth", id="bluetooth", variant="primary")
        yield Button("Device", id="device")

class PiRaiderApp(App):
    """PiRaider TUI app."""

    CSS_PATH = "stylesheet.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit the app")
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield CustomHeader()
        yield Footer()
        yield BucketsGroup()

    def on_mount(self) -> None:
        self.refresh_header_from_config()

    def refresh_header_from_config(self) -> None:
        """Set header radio button values from config key existence only."""
        try:
            header = self.query_one(CustomHeader)
            header.query_one("#wifi_status", RadioButton).value = has_key("wifi_device")
            header.query_one("#bluetooth_status", RadioButton).value = has_key(
                "bluetooth_device"
            )
        except Exception:
            pass

    def on_radio_button_changed(self, event: RadioButton.Changed) -> None:
        """Navigate to WiFi screen when the user taps the WiFi status in the header."""
        if event.radio_button.id == "wifi_status":
            self.push_screen(WifiConfigScreen())
        if event.radio_button.id == "bluetooth_status":
            self.push_screen(BluetoothConfigScreen())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

def tui_main():
    app = PiRaiderApp()
    app.run()