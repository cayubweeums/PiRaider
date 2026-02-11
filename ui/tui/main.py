from rich.console import Console


console = Console(
    color_system="auto"
)

def tui_main():
    console.log("Hello, World! LOG")
    console.print("Hello, World! PRINT")
