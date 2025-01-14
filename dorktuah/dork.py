from typing import Literal, Optional, List, Dict
from .proxy import ProxyManager
from seleniumbase import Driver
from selenium.common.exceptions import JavascriptException, WebDriverException
from bs4 import BeautifulSoup
from urllib.parse import unquote
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

@dataclass
class SearchResult:
    """Data class to represent search results"""
    url: str
    title: str  
    description: str

class SearchEngine:
    """Base class for search engine implementations"""
    def __init__(self, driver: Driver):
        self.driver = driver
    
    def search(self, query: str) -> List[SearchResult]:
        raise NotImplementedError
        
    def get_next_page(self) -> List[SearchResult]:
        raise NotImplementedError
        
    def has_next_page(self) -> bool:
        raise NotImplementedError

class EtoolsEngine(SearchEngine):
    """ETools search engine implementation"""
    
    BASE_URL = "https://www.etools.ch/search.do"
    
    def __init__(self, driver: Driver):
        super().__init__(driver)
        
    def _parse_results(self, html: str) -> List[SearchResult]:
        """Parse HTML and extract search results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for row in soup.find_all('tr'):
            record = row.find('td', {'class': 'record'})
            if not record:
                continue
                
            title = record.find('a', {'class': 'title'})
            description = record.find('div', {'class': 'text'})
            if not (title and description):
                continue
                
            url = title.get("href", "")
            if url.startswith("redirect.do?a="):
                url = unquote(url.replace("redirect.do?a=",""))
                
            results.append(SearchResult(
                url=url.strip(),
                title=title.text.strip(),
                description=description.text.strip()
            ))
            
        return results

    def _load_more_results(self):
        """Load additional results via pagination"""
        selector = "form table tr:nth-child(3) td:nth-child(2) p.resultStatus a"
        while True:
            try:
                a_tag = self.driver.find_element(selector)
                if not (a_tag and "more" in a_tag.text.lower()):
                    break
                a_tag.click()
                self.driver.sleep(1)
            except WebDriverException:
                break

    def search(self, query: str) -> List[SearchResult]:
        """Perform search and return results"""
        try:
            self.driver.uc_open(self.BASE_URL)
            self.driver.type("input[type='search']", query)
            self.driver.click("input[type='submit']")
            self.driver.sleep(1)
            
            # Accept cookies
            self.driver.execute_script(
                "document.querySelector('.cmpwrapper').shadowRoot.getElementById('cmpbntyestxt').click()"
            )
            self.driver.sleep(2)
            
            self.driver.click("input[type='submit']")
            self._load_more_results()
            
            return self._parse_results(self.driver.get_page_source())
            
        except JavascriptException:
            logger.error("Proxy connection failed")
            raise RuntimeError("Proxy unreliable - please ensure proxies are working")
        except WebDriverException as e:
            logger.error(f"Search failed: {str(e)}")
            raise

    def has_next_page(self) -> bool:
        """Check if next page exists"""
        try:
            nav = self.driver.find_element("p.pageNav")
            next_link = self.driver.find_element("p.pageNav a:last-child")
            return bool(nav and next_link)
        except WebDriverException:
            return False

    def get_next_page(self) -> List[SearchResult]:
        """Get results from next page"""
        if not self.has_next_page():
            return []
            
        self.driver.find_element("p.pageNav a:last-child").click()
        self.driver.sleep(1)
        return self._parse_results(self.driver.get_page_source())

class Dorktuah:
    """Main search interface"""
    
    def __init__(
        self,
        proxy_type: Literal["socks4", "socks5", "http", "all"] = "all",
        use_proxy: bool = True,
        use_custom: bool = True,
        source_limit: int = 10,
        proxy_path: str = None
    ):
        self.proxy_manager = ProxyManager(
            proxy_type=proxy_type,
            use_proxy=use_proxy, 
            use_custom=use_custom,
            source_limit=source_limit,
            proxy_path=proxy_path
        )
        self.driver: Optional[Driver] = None
        self.engine: Optional[SearchEngine] = None
        
    def _initialize(self):
        """Initialize driver and search engine"""
        if not self.driver:
            proxy = self.proxy_manager.get_proxy() if self.proxy_manager.use_proxy else None
            self.driver = Driver(uc=True, headless2=True, proxy=proxy)
            self.engine = EtoolsEngine(self.driver)
            
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.engine = None
            
    def search(self, query: str) -> List[SearchResult]:
        """Perform search"""
        self._initialize()
        return self.engine.search(query)
        
    def has_next_page(self) -> bool:
        """Check for next page"""
        return bool(self.engine and self.engine.has_next_page())
        
    def get_next_page(self) -> List[SearchResult]:
        """Get next page results"""
        return self.engine.get_next_page() if self.engine else []