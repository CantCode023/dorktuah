from typing import Literal
from bs4.element import nonwhitespace_re
import random, requests
from pathlib import Path

def ProxyPool(type:Literal["socks4", "socks5", "http", "all"] = "all"):
    def __get_proxies():
        with open(Path(__file__).parent/"proxies.txt", "r") as f:
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
        
    proxies = __get_proxies()
    
    if type != "all":
        proxies = list(filter(lambda x: x.startswith(type), proxies))
    
    i=0
    while True:
        proxy = proxies[i]
        print("[!] Trying", proxy)
        if __check(proxy):
            print("[!] Found working!")
            return {"http": proxy, "https": proxy}
        i+=1
        print("[!] Failed!")