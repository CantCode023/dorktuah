import requests
import logging
from typing import Literal, Optional
from pathlib import Path
from .scraper import AsyncProxyScraper, scrape_proxies

logger = logging.getLogger(__name__)

class ProxyManager:
    """Manages proxy selection and validation"""
    
    def __init__(
        self,
        proxy_type: Literal["socks4", "socks5", "http", "all"] = "all",
        use_proxy: bool = True,
        use_custom: bool = True,
        source_limit: int = 10,
        proxy_path: Optional[str] = None
    ):
        self.proxy_type = proxy_type
        self.use_proxy = use_proxy
        self.use_custom = use_custom
        self.source_limit = source_limit
        self.proxy_path = proxy_path or str(Path(__file__).parent / "proxies.txt")
        
    def _load_proxies(self) -> list[str]:
        """Load proxies from file or scraper"""
        if self.use_custom:
            try:
                with open(self.proxy_path) as f:
                    proxies = [line.strip() for line in f if line.strip()]
                logger.info(f"Loaded {len(proxies)} proxies from file")
                return proxies
            except IOError as e:
                logger.error(f"Failed to load proxies: {e}")
                return []
        else:
            logger.info("Scraping proxies asynchronously...")
            return scrape_proxies(self.source_limit)
            
    def _filter_proxies(self, proxies: list[str]) -> list[str]:
        """Filter proxies by type"""
        if self.proxy_type == "all":
            return proxies
        return [p for p in proxies if p.startswith(self.proxy_type)]
        
    def _check_proxy(self, proxy: str) -> bool:
        """Validate proxy connectivity"""
        try:
            response = requests.get(
                "https://google.com",
                proxies={"http": proxy, "https": proxy},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Proxy check failed: {proxy} - {e}")
            return False
            
    def get_proxy(self) -> Optional[str]:
        """Get working proxy"""
        if not self.use_proxy:
            return None
            
        proxies = self._filter_proxies(self._load_proxies())
        if not proxies:
            logger.error("No proxies available")
            return None
            
        for proxy in proxies:
            logger.info(f"Testing proxy: {proxy}")
            if self._check_proxy(proxy):
                logger.info(f"Found working proxy: {proxy}")
                return proxy
                
        logger.error("No working proxies found")
        return None