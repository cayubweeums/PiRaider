from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button


class CustomHeader(Horizontal):
    """Header showing WiFi/Bluetooth status; click opens the config screen."""

    def compose(self) -> ComposeResult:
        """Create child widgets (labels updated from config by app)."""
        yield Button("WiFi", id="wifi_status", variant="default")
        yield Button("Bluetooth", id="bluetooth_status", variant="default")