from typing import Literal, Optional
from seleniumbase import SB
from bs4 import BeautifulSoup

class Engine:
    def __init__(
        self,
        proxy_type:Literal["socks4", "socks5", "http", "all"] = "all",
        use_proxy:bool=True,
        use_custom:bool=True,
        proxy_path:str=""
    ):
        self.proxy_type = proxy_type
        self.use_proxy = use_proxy
        self.use_custom = use_custom
        self.proxy_path = proxy_path
        
    def search(self, query):
        results = []
        source = ""

        with SB(uc=True, headless2=True) as sb:
            sb.open("https://www.etools.ch/search.do")
            sb.type("input[type='search']", query)
            sb.type("input[type='submit']", query)
            if sb.is_element_visible("a.cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes"):
                sb.click("a.cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes")
            source = sb.get_page_source()
            
        soup = BeautifulSoup(source, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            record = row.find('td', {'class': 'record'})
            if record:
                title = record.find('a', {'class': 'title'})
                description = record.find('div', {'class': 'text'})
                if title and description:
                    result = {
                        "url": title.get("href"),
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