from typing import Literal, Optional

class Engine:
    def __init__(
        self,
        site:str="https://www.google.com/search?q=",
        num:int=10,
        start:int=0,
        end:int=10,
        proxy_type:Literal["socks4", "socks5", "http", "all"] = "all",
        use_proxy:bool=True,
        use_custom:bool=True,
        proxy_path:str=""
    ):
        self.site = site
        self.num = num
        self.start = start
        self.end = end
        self.proxy_type = proxy_type
        self.use_proxy = use_proxy
        self.use_custom = use_custom
        self.proxy_path = proxy_path