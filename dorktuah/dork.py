from .modules.engine import Engine
from typing import Literal

def dork(
    query, 
    proxy_type:Literal["socks4", "socks5", "http", "all"]="all", 
    use_proxy:bool=True, 
    use_custom:bool=True, 
    source_limit:int=10,
    proxy_path="C:/Users/cantc/Desktop/Coding/Python/dorktuah/dorktuah/modules/proxy/proxies.txt"
):
    engine = Engine(proxy_type=proxy_type, use_proxy=use_proxy, use_custom=use_custom, source_limit=source_limit, proxy_path=proxy_path)
    results = engine.search(query)
    return results