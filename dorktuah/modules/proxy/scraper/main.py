from typing import Literal
from pathlib import Path
import toml, requests

with open(Path(__file__).parent/"config.toml", "r") as f:
    config = toml.load(f)

http_sources = config["http"]["sources"]
socks4_sources = config["socks4"]["sources"]
socks5_sources = config["socks5"]["sources"]

def scrape_proxies():
    proxies = []
    for source in http_sources+socks4_sources+socks5_sources:
        try:
            response = requests.get(source)
            if response.status_code == 200:
                for proxy in response.text.splitlines():
                    proxy = proxy.strip()
                    if proxy:
                        proxies.append(proxy)
        except:
            continue
    return proxies