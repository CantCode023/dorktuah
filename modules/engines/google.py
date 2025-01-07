from ..proxy import ProxyPool
from ..engine import Engine
import requests, urllib.parse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Google(Engine):
    def search(self, query):
        self.site = "https://www.google.com/search?q="
        headers = {"User-Agent": UserAgent().random}
        if self.use_proxy:
            proxy = ProxyPool(self.proxy_type)
            response = requests.get(f"{self.site+urllib.parse.quote(query)}", headers=headers, proxies=proxy, timeout=10)
        else:
            response = requests.get(f"{self.site+urllib.parse.quote(query)}", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for title in soup.find_all('h3'):
            results.append(title.text)
        return results