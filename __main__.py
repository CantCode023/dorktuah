import os, textwrap, json, time
from dorktuah import Dorktuah
from seleniumbase import colorama
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import print as rprint
from rich.pretty import pprint
from colorama import Fore, Style, init
init(convert=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(options:str="\n[0] Query\n[1] Proxy Settings\n[2] Exit"):
    clear()
    title = """
    ██████╗  █████╗ ██████╗ ██╗  ██╗████████╗██╗   ██╗ █████╗ ██╗  ██╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚══██╔══╝██║   ██║██╔══██╗██║  ██║
    ██║  ██║██║  ██║██████╔╝█████═╝    ██║   ██║   ██║███████║███████║
    ██║  ██║██║  ██║██╔══██╗██╔═██╗    ██║   ██║   ██║██╔══██║██╔══██║
    ██████╔╝╚█████╔╝██║  ██║██║ ╚██╗   ██║   ╚██████╔╝██║  ██║██║  ██║
    ╚═════╝  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
    """
    
    rprint(f"[bright_white][b]{title}[/b][/bright_white]")
    rprint(f"[white][i]Dork across search engines.[/i][/white]")
    
    rprint(f"\n[bright_white]--------------------------------------------[/bright_white]")
    rprint("[white]Author: CantCode023[/white]")
    rprint("[white]Github: github.com/CantCode023/dorktuah[/white]")
    rprint("[white]Discord: bd8344[/white]")
    if options != "":
        rprint(options)
    rprint(f"[bright_white]--------------------------------------------[/bright_white]\n")

def load_config():
    with open("./dorktuah/config.json", "r") as f:
        config = json.load(f) 
    return config

def print_results(results):
    for i, result in enumerate(results):
        title = result["title"].strip()
        description = result["description"].strip()
        url = result["url"].strip()
    
        wrapped_title = textwrap.fill(title, width=80, subsequent_indent="\t    ")
        wrapped_description = textwrap.fill(description, width=80, subsequent_indent="\t    ")
    
        print(Style.BRIGHT + Fore.WHITE + f"{i+1}. ——— Title: " + Fore.MAGENTA + wrapped_title)
        print("\t" + Style.BRIGHT + Fore.WHITE + f"Description: {Fore.LIGHTGREEN_EX + wrapped_description}")
        print("\t" + Style.BRIGHT + Fore.WHITE + f"Link: {Fore.LIGHTBLUE_EX + url}")
        print("\n")

def show_query():
    show_menu("")
    query = Prompt.ask("[blue]Query[/blue]", default="Type /back to go back")
    if query == "/back":
        return
    
    config = load_config()
    
    dorktuah = Dorktuah(
        proxy_type=config["proxy_type"],
        use_proxy=config["enabled"],
        use_custom=config["use_custom"],
        proxy_path=config["proxy_path"],
        source_limit=config["source_limit"]
    )
    
    results = dorktuah.search(query)
    print_results(results)
        
    while True:
        has_next_page = dorktuah.has_next_page()
        if has_next_page:
            print(Style.DIM + Fore.LIGHTBLUE_EX + "Press enter to go next...")
        print(Style.DIM + Fore.LIGHTRED_EX + "Type q and press enter to go back...")
        inp = input()
        if inp.lower() == "q":
            dorktuah.close()
            return
        show_menu("")
        results = dorktuah.get_next_page()
        print_results(results)
        
def show_proxy():
    config = load_config()
        
    while True:
        show_menu("\n[0] Enable proxy\n[1] Use custom proxy\n[2] Proxy type\n[3] Proxy path\n[4] Scraping source limit\n[5] Save\n[6] Show config\n[7] Back\n[8] Exit")
    
        option = int(Prompt.ask("[blue]Enter number[/blue]"))
        if option == 0:
            enable = Confirm.ask("[blue]Enable proxy[/blue]")
            config["enabled"] = enable
        elif option == 1:
            use_custom = Confirm.ask("[blue]Use custom proxy[/blue]")
            config["use_custom"] = use_custom
        elif option == 2:
            proxy_type = Prompt.ask("[blue]Proxy type[/blue]", choices=["socks4", "socks5", "http", "all"])
            config["proxy_type"] = proxy_type.lower()
        elif option == 3:
            proxy_path = Prompt.ask("[blue]Proxy path (absolute, path to your proxy list e.g C:/.../proxy.txt)[/blue]")
            if not os.path.exists(proxy_path):
                rprint("[red]File doesn't exist![/red]")
                rprint("[blue]Press enter to continue...[/blue]")
                input()
                continue 
            config["proxy_path"] = proxy_path
        elif option == 4:
            int_choices = [str(i) for i in range(1,101)]
            source_limt = int(Prompt.ask("[blue]Scraping source limit[/blue]", default="[1-100]"))
            config["source_limit"] = source_limt
        elif option == 5:
            try:
                with open("./dorktuah/config.json", "w") as f:
                    json.dump(config, f, indent=4)
                rprint("[green]Config saved successfully![/green]")
            except Exception as e:
                rprint(f"[red]Error while saving config: {str(e)}[/red]")
            rprint("[blue]Press enter to continue...[/blue]")
            input()
        elif option == 6:
            pprint(config)
            rprint("[blue]Press enter to continue...[/blue]")
            input()
        elif option == 7:
            return False
        elif option == 8:
            return True
    
if __name__ == "__main__":
    config = {
        "enabled": False,
        "use_custom": False,
        "proxy_type": "all",
        "proxy_path": "C:/Users/cantc/Desktop/Coding/Python/dorktuah/dorktuah/proxy/proxies.txt",
        "source_limit": 10
    }
    
    if not os.path.exists("./dorktuah/config.json"):
        rprint("[red]Config file not found! Creating one.[/red]")
        with open("./dorktuah/config.json", "w") as f:
            json.dump(config, f, indent=4) 
        rprint("[green]Successfully created config file. Click enter to continue[/green]")
        input()
    
    while True:
        show_menu()
        option = int(Prompt.ask("[blue]Enter number[/blue]", choices=['0', '1', '2'], show_choices=True))
        if option == 0:
            show_query()
        elif option == 1:
            is_break = show_proxy()
            if is_break:
                rprint("[blue]Goodbye![/blue]")
                break
        elif option == 2:
            rprint("[blue]Goodbye![/blue]")
            break