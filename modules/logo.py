import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class LOGO:
    def __init__(self,logo):
        self.logo = logo
        self.console = Console()
    
    def draw_LG(self):
    
        self.console.print(Panel(Text("Welcome To Hacker Space", justify="center", style="bold red"), border_style="red"))

        logo_text_2 = pyfiglet.figlet_format(self.logo, font="doom")
        styled_logo_2 = f"[bold red on black]{logo_text_2}[/bold red on black]"

        self.console.print(Text.from_markup(styled_logo_2, justify="center"))
        
        self.console.print(Text("---Vulnerability web-server Scanner---", justify="center", style="bold orange1"))
        self.console.print("\n")
