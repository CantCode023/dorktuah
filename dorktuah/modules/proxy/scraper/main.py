from typing import Literal
from pathlib import Path
import toml, requests

with open(Path(__file__).parent/"config.toml", "r") as f:
    config = toml.load(f)

http_sources = config["http"]["sources"]
socks4_sources = config["socks4"]["sources"]
socks5_sources = config["socks5"]["sources"]
all_sources = http_sources+socks4_sources+socks5_sources

def scrape_proxies(source_limit:int=10):
    proxies = []
    print("[!] Scraping proxies.")
    limited = all_sources if source_limit == None else all_sources[:source_limit]
    for source in limited:
        try:
            response = requests.get(source)
            if response.status_code == 200:
                print(f"[!] Scraped proxy from {source}")
                for proxy in response.text.splitlines():
                    proxy = proxy.strip()
                    if proxy:
                        proxies.append(proxy)
        except:
            continue
    print("[!] Scraping finished!")
    return proxies