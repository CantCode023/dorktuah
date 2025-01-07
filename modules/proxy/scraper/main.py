from typing import Literal
from pathlib import Path
import toml, requests

with open(Path(__file__).parent/"config.toml", "r") as f:
    config = toml.load(f)

http_sources = config["http"]["sources"]
socks4_sources = config["socks4"]["sources"]
socks5_sources = config["socks5"]["sources"]

def scrape_proxies(type:Literal["socks4", "socks5", "http", "all"]="all"):
    http_proxies, socks4_proxies, socks5_proxies = [], [], []
    for source in http_sources:
        try:
            response = requests.get(source)
            proxies = response.text.strip().split("\n")
            http_proxies.extend(proxies)
        except:
            continue
    for source in socks4_sources:
        try:
            response = requests.get(source)
            proxies = response.text.strip().split("\n")
            socks4_proxies.extend(proxies)
        except:
            continue
    for source in socks5_sources:
        try:
            response = requests.get(source)
            proxies = response.text.strip().split("\n")
            socks5_proxies.extend(proxies) 
        except:
            continue 
    if type == "all":
        return http_proxies+socks4_proxies+socks5_proxies
    elif type == "http":
        return http_proxies
    elif type == "socks4":
        return socks4_proxies
    elif type == "socks5":
        return socks5_proxies