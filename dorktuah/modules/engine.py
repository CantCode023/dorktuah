from typing import Literal, Optional
from seleniumbase import SB
from selenium.common.exceptions import JavascriptException
from bs4 import BeautifulSoup
from .proxy import ProxyPool
from urllib.parse import unquote

class Engine:
    def __init__(
        self,
        proxy_type:Literal["socks4", "socks5", "http", "all"] = "all",
        use_proxy:bool=True,
        use_custom:bool=True,
        source_limit:int=10,
        proxy_path:str="C:/Users/cantc/Desktop/Coding/Python/dorktuah/dorktuah/modules/proxy/proxies.txt"
    ):
        self.proxy_type = proxy_type
        self.use_proxy = use_proxy
        self.use_custom = use_custom
        self.source_limit = source_limit
        self.proxy_path = proxy_path
        
    def search(self, query):
        results = []
        source = ""
        proxy = None

        if self.use_proxy:
            proxy = ProxyPool(type=self.proxy_type, use_custom=self.use_custom, proxy_path=self.proxy_path, source_limit=self.source_limit)

        try:
            with SB(uc=True, headless2=True, proxy=proxy) as sb:
                sb.open("https://www.etools.ch/search.do")
                sb.type("input[type='search']", query)
                sb.click("input[type='submit']")
                sb.sleep(1)
                sb.execute_script("document.querySelector('.cmpwrapper').shadowRoot.getElementById('cmpbntyestxt').click()") 
                sb.sleep(1)
                sb.click("input[type='submit']")
                source = sb.get_page_source()
        except JavascriptException:
            print("[!] Proxy unreliable, please ensure your proxies are working and stable. If you think this is wrong, try again.")
            
        soup = BeautifulSoup(source, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            record = row.find('td', {'class': 'record'})
            if record:
                title = record.find('a', {'class': 'title'})
                description = record.find('div', {'class': 'text'})
                if title and description:
                    url = title.get("href")
                    url = unquote(url.replace("redirect.do?a=","")) if url.startswith("redirect.do?a=") else url
                    result = {
                        "url": url,
                        "title": title.text,
                        "description": description.text
                    }
                    results.append(result)

        unique_urls = set()
        unique_results = []
        for result in results:
            if result["url"] not in unique_urls:
                unique_urls.add(result["url"])
                unique_results.append(result)
        results = unique_results
        return results