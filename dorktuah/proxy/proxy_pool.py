from typing import Literal
from pathlib import Path
from .scraper import scrape_proxies
import random, requests

def ProxyPool(type:Literal["socks4", "socks5", "http", "all"] = "all", use_custom:bool=True, proxy_path:str="C:/Users/cantc/Desktop/Coding/Python/dorktuah/dorktuah/proxy/proxies.txt", source_limit:int=10):
    def __get_proxies():
        with open(proxy_path, "r") as f:
            proxies = [line.strip() for line in f.readlines()]
        return proxies
        
    def __check(proxy):
        try:
            response = requests.get("https://google.com", proxies={
                "http": proxy,
                "https": proxy
            }, timeout=10)
            if response.status_code == 200:
                return True
        except:
            return False
        return False 
        
    proxies = __get_proxies() if use_custom else scrape_proxies(source_limit)
    
    if type != "all":
        proxies = list(filter(lambda x: x.startswith(type), proxies))
    
    i=0
    while True:
        proxy = proxies[i]
        print("[!] Trying", proxy)
        if __check(proxy):
            print("[!] Found working!")
            return proxy
        i+=1
        print("[!] Failed!")