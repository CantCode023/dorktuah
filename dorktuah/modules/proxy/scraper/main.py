from typing import Literal
from pathlib import Path
import toml, requests

with open(Path(__file__).parent/"config.toml", "r") as f:
    config = toml.load(f)

http_sources = config["http"]["sources"]
socks4_sources = config["socks4"]["sources"]
socks5_sources = config["socks5"]["sources"]
all_sources = http_sources+socks4_sources+socks5_sources

def get_proxy_protocol(source: str) -> str:
    """Determine proxy protocol based on source URL."""
    if source in http_sources:
        return "http"
    elif source in socks4_sources:
        return "socks4"
    elif source in socks5_sources:
        return "socks5"
    return ""

def parse_proxy_line(line: str, protocol: str) -> str:
    """Parse a single proxy line and return formatted proxy address."""
    proxy = line.strip()
    return f"{protocol}://{proxy}" if proxy else ""

def scrape_single_source(source: str) -> list:
    """Scrape proxies from a single source URL."""
    try:
        response = requests.get(source)
        if response.status_code != 200:
            print(f"[!] Failed to scrape from {source}: Status {response.status_code}")
            return []
            
        print(f"[!] Successfully scraped from {source}")
        protocol = get_proxy_protocol(source)
        
        return [
            parse_proxy_line(line, protocol)
            for line in response.text.splitlines()
            if line.strip()
        ]
        
    except Exception as e:
        print(f"[!] Error scraping from {source}: {str(e)}")
        return []

def scrape_proxies(source_limit: int = 10) -> list:
    """
    Scrape proxies from multiple sources.
    Args:
        source_limit: Maximum number of sources to scrape from. None for all sources.
    Returns:
        List of formatted proxy addresses
    """
    print("[!] Starting proxy scraping...")
    
    sources = all_sources if source_limit is None else all_sources[:source_limit]
    proxies = []
    
    for source in sources:
        proxies.extend(scrape_single_source(source))
        
    print(f"[!] Scraping finished! Found {len(proxies)} proxies")
    return proxies