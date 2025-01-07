from ..proxy import ProxyPool
from ..engine import Engine
import requests, urllib.parse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Google(Engine):
    def search(self, query):
        self.site = "https://www.google.com/search?q="
        url = f"{self.site+urllib.parse.quote(query)}&num={self.num}&start={self.start}"
        headers = {"User-Agent": UserAgent().random}
        if self.use_proxy:
            proxy = ProxyPool(self.proxy_type, use_custom=self.use_custom)
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        else:
            response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for title in soup.find_all('h3'):
            results.append(title.text)
        return results