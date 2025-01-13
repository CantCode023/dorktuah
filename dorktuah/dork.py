# from typing import Literal, Optional
# from seleniumbase import Driver
# from selenium.common.exceptions import JavascriptException
# from bs4 import BeautifulSoup
# from .proxy import ProxyPool
# from urllib.parse import unquote

# class Dorktuah:
#     def __init__(
#         self,
#         proxy_type:Literal["socks4", "socks5", "http", "all"] = "all",
#         use_proxy:bool=True,
#         use_custom:bool=True,
#         source_limit:int=10,
#         proxy_path:str="C:/Users/cantc/Desktop/Coding/Python/dorktuah/dorktuah/proxy/proxies.txt"
#     ):
#         self.proxy_type = proxy_type
#         self.use_proxy = use_proxy
#         self.use_custom = use_custom
#         self.source_limit = source_limit
#         self.proxy_path = proxy_path
#         self.running = True
#         self.result = {}
    
    # def get_source(self, self.driver):
    #     container = self.driver.find_element("body > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > table > tbody")
    #     return container if container else self.driver.get_page_source()
        
#     def load_more_results(self, self.driver):
#         selector = """body > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > p.resultStatus > a"""
#         a_tag = self.driver.find_element(selector)
#         while a_tag and "more" in a_tag.text.lower():
#             a_tag.click()
#             self.driver.sleep(1)
#             a_tag = self.driver.find_element(selector)
#             if a_tag: continue
#             else: break
            
#     def pagination(self, self.driver):
#         have_pages = self.driver.find_element("p.pageNav")
#         sources = []
#         if have_pages:
#             while True:
#                 have_next = self.driver.find_element("body > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > p.pageNav > a:nth-child(9)")
#                 if have_next:
#                     have_next.click()
#                     self.driver.sleep(1)
#                     sources.append(self.__get_source(self.driver)) 
#                 else: break
            
#             return sources
#         return [self.__get_source(self.driver)]
        
#     def open(self, query):
#         sources = []
#         proxy = None

#         if self.use_proxy:
#             proxy = ProxyPool(type=self.proxy_type, use_custom=self.use_custom, proxy_path=self.proxy_path, source_limit=self.source_limit)

#         self.driver = Driver(uc=True, headless2=True, proxy=proxy)
#         try:
#             self.driver.open("https://www.etools.ch/search.do")
#             self.driver.type("input[type='search']", query)
#             self.driver.click("input[type='submit']")
#             self.driver.sleep(1)
#             self.driver.execute_script("document.querySelector('.cmpwrapper').shadowRoot.getElementById('cmpbntyestxt').click()") 
#             self.driver.sleep(1)
#             self.driver.click("input[type='submit']")
#             self.__get_more_results(self.driver)
#             sources = self.__pagination(self.driver)
#         except JavascriptException:
#             print("[!] Proxy unreliable, please ensure your proxies are working and stable. If you think this is wrong, try again.")
            
#         return sources
    

from typing import Literal
from .proxy import ProxyPool
from seleniumbase import Driver
from selenium.common.exceptions import JavascriptException
from bs4 import BeautifulSoup
from urllib.parse import unquote
 
class Dorktuah:
    def __init__(self,
        proxy_type:Literal["socks4", "socks5", "http", "all"] = "all",
        use_proxy:bool=True,
        use_custom:bool=True,
        source_limit:int=10,
        proxy_path:str="C:/Users/cantc/Desktop/Coding/Python/dorktuah/dorktuah/proxy/proxies.txt"
    ):
        self.proxy_type = proxy_type
        self.use_proxy = use_proxy
        self.use_custom = use_custom
        self.source_limit = source_limit
        self.proxy_path = proxy_path
        
        self.driver:Driver=None
        
    def open(self):
        proxy = ""
        if self.use_proxy:
            proxy = ProxyPool(type=self.proxy_type, use_custom=self.use_custom, proxy_path=self.proxy_path, source_limit=self.source_limit)
        
        driver:Driver = Driver(uc=True, headless2=True, proxy=proxy)
        self.driver = driver
        
    def close(self):
        self.driver.quit()
        if self.driver: self.driver = None
        
    def get_results(self, source):
        results = []
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
        return results
        
    def load_more_results(self):
        selector = "form table tr:nth-child(3) td:nth-child(2) p.resultStatus a"
        a_tag = self.driver.find_element(selector)
        while a_tag and "more" in a_tag.text.lower():
            a_tag.click()
            self.driver.sleep(1)
            a_tag = self.driver.find_element(selector)
            if a_tag: continue
            else: break
            
    def has_next_page(self):
        try: 
            has_page = self.driver.find_element("p.pageNav")
            if has_page:
                has_next = self.driver.find_element("p.pageNav a:last-child") 
                if has_next: return has_next
        except:
            return None
        
    def get_next_page(self):
        has_next_page = self.has_next_page()
        if has_next_page:
            has_next_page.click()
            self.driver.sleep(1)
            return self.get_results(self.driver.get_page_source())
       
    def search(self, query):
        if self.driver == None:
            self.open()
        try:
            self.driver.uc_open("https://www.etools.ch/search.do")
            self.driver.type("input[type='search']", query)
            self.driver.click("input[type='submit']")
            self.driver.sleep(1)
            self.driver.execute_script("document.querySelector('.cmpwrapper').shadowRoot.getElementById('cmpbntyestxt').click()") 
            self.driver.sleep(2)
            self.driver.click("input[type='submit']")
            self.load_more_results()
            source = self.driver.get_page_source()
            return self.get_results(source)
        except JavascriptException:
            print("[!] Proxy unreliable, please ensure your proxies are working and stable. If you think this is wrong, try again.")