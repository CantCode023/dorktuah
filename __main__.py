import os, textwrap, json
from typing import Dict, Optional, List
from pathlib import Path
from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.theme import Theme
from rich.panel import Panel
from dorktuah import Dorktuah, SearchResult

@dataclass
class Config:
    enabled: bool = False
    use_custom: bool = False
    proxy_type: str = "all"
    proxy_path: str = str(Path(__file__).parent / "dorktuah/proxy/proxies.txt")
    source_limit: int = 10
    
    @classmethod
    def load(cls, path: str) -> 'Config':
        """Load config from JSON file"""
        try:
            with open(path) as f:
                data = json.load(f)
            return cls(**data)
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            return cls()
            
    def save(self, path: str) -> bool:
        """Save config to JSON file"""
        try:
            with open(path, 'w') as f:
                json.dump(self.__dict__, f, indent=4)
            return True
        except Exception as e:
            console.print(f"[red]Error saving config: {e}[/red]")
            return False

class DorktuahCLI:
    """Command line interface for Dorktuah"""
    
    TITLE = """
██████╗  █████╗ ██████╗ ██╗  ██╗████████╗██╗   ██╗ █████╗ ██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚══██╔══╝██║   ██║██╔══██╗██║  ██║
██║  ██║██║  ██║██████╔╝█████═╝    ██║   ██║   ██║███████║███████║
██║  ██║██║  ██║██╔══██╗██╔═██╗    ██║   ██║   ██║██╔══██║██╔══██║
██████╔╝╚█████╔╝██║  ██║██║ ╚██╗   ██║   ╚██████╔╝██║  ██║██║  ██║
╚═════╝  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
    """
    
    def __init__(self):
        self.config_path = Path(__file__).parent / "dorktuah/config.json"
        self.config = self._init_config()
        self.dorktuah: Optional[Dorktuah] = None
        
    def _init_config(self) -> Config:
        """Initialize configuration"""
        if not self.config_path.exists():
            console.print("[yellow]Config file not found! Creating default...[/yellow]")
            config = Config()
            config.save(self.config_path)
            return config
        return Config.load(self.config_path)
        
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_header(self, options: str = ""):
        """Display application header"""
        self.clear_screen()
        console.print(Panel.fit(
            f"[bright_white]{self.TITLE}[/bright_white]\n"
            "[italic]Dork across search engines.[/italic]\n\n"
            "[white]Author: CantCode023[/white]\n"
            "[white]Github: github.com/CantCode023/dorktuah[/white]\n"
            "[white]Discord: bd8344[/white]" +
            (f"\n{options}" if options else ""),
        ))
        
    def print_results(self, results: List[SearchResult]):
        """Display search results"""
        for i, result in enumerate(results, 1):
            title = textwrap.fill(
                result.title,
                width=80,
                subsequent_indent="\t    "
            )
            description = textwrap.fill(
                result.description,
                width=80,
                subsequent_indent="\t    "
            )
            
            console.print(f"[bold white]{i}. ——— Title:[/bold white] [magenta]{title}[/magenta]")
            console.print(f"\t[bold white]Description:[/bold white] [green]{description}[/green]")
            console.print(f"\t[bold white]Link:[/bold white] [blue]{result.url}[/blue]\n")
            
    def handle_search(self):
        """Handle search functionality"""
        self.show_header()
        query = Prompt.ask("[blue]Query[/blue]", default="Type /back to go back")
        if query.lower() == "/back":
            return
            
        self.dorktuah = Dorktuah(
            proxy_type=self.config.proxy_type,
            use_proxy=self.config.enabled,
            use_custom=self.config.use_custom,
            proxy_path=self.config.proxy_path,
            source_limit=self.config.source_limit
        )
        
        try:
            results = self.dorktuah.search(query)
            self.print_results(results)
            
            while True:
                if self.dorktuah.has_next_page():
                    console.print("[blue]Press enter to go next...[/blue]")
                console.print("[red]Type q and press enter to go back...[/red]")
                
                if (inp := input().lower()) == "q":
                    break
                    
                self.show_header()
                results = self.dorktuah.get_next_page()
                self.print_results(results)
                
        finally:
            if self.dorktuah:
                self.dorktuah.close()
                
    def handle_proxy_settings(self) -> bool:
        """Handle proxy configuration"""
        while True:
            self.show_header(
                "\n[0] Enable proxy\n[1] Use custom proxy\n"
                "[2] Proxy type\n[3] Proxy path\n[4] Scraping source limit\n"
                "[5] Save\n[6] Show config\n[7] Back\n[8] Exit"
            )
            
            option = Prompt.ask("[blue]Enter number[/blue]", choices=[str(i) for i in range(9)])
            
            if option == "0":
                self.config.enabled = Confirm.ask("[blue]Enable proxy[/blue]")
            elif option == "1":
                self.config.use_custom = Confirm.ask("[blue]Use custom proxy[/blue]")
            elif option == "2":
                self.config.proxy_type = Prompt.ask(
                    "[blue]Proxy type[/blue]",
                    choices=["socks4", "socks5", "http", "all"]
                ).lower()
            elif option == "3":
                proxy_path = Prompt.ask(
                    "[blue]Proxy path (absolute path to proxy list)[/blue]"
                )
                if not Path(proxy_path).exists():
                    console.print("[red]File doesn't exist![/red]")
                    self.wait_for_input()
                    continue
                self.config.proxy_path = proxy_path
            elif option == "4":
                self.config.source_limit = int(Prompt.ask(
                    "[blue]Scraping source limit[/blue]",
                    default="10"
                ))
            elif option == "5":
                if self.config.save(self.config_path):
                    console.print("[green]Config saved successfully![/green]")
                self.wait_for_input()
            elif option == "6":
                console.print_json(data=self.config.__dict__)
                self.wait_for_input()
            elif option == "7":
                return False
            elif option == "8":
                return True
                
    @staticmethod
    def wait_for_input():
        """Wait for user input"""
        console.print("[blue]Press enter to continue...[/blue]")
        input()
        
    def run(self):
        """Main application loop"""
        while True:
            self.show_header("\n[0] Query\n[1] Proxy Settings\n[2] Exit")
            option = Prompt.ask(
                "[blue]Enter number[/blue]",
                choices=['0', '1', '2'],
                show_choices=True
            )
            
            if option == "0":
                self.handle_search()
            elif option == "1":
                if self.handle_proxy_settings():
                    break
            else:
                break
                
        console.print("[blue]Goodbye![/blue]")

# Initialize rich console with custom theme
console = Console(theme=Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "error": "bold red"
}))

if __name__ == "__main__":
    cli = DorktuahCLI()
    cli.run()