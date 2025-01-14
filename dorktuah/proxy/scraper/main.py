import toml, asyncio, aiohttp, logging
from typing import Optional, List
from pathlib import Path
from asyncio import gather
from aiohttp import ClientTimeout

logger = logging.getLogger(__name__)

class AsyncProxyScraper:
    """Asynchronous proxy scraper for multiple sources"""
    
    def __init__(self):
        self.config = self._load_config()
        self.http_sources = self.config["http"]["sources"]
        self.socks4_sources = self.config["socks4"]["sources"] 
        self.socks5_sources = self.config["socks5"]["sources"]
        self.timeout = ClientTimeout(total=10)
        
    def _load_config(self) -> dict:
        """Load scraper configuration"""
        config_path = Path(__file__).parent / "config.toml"
        try:
            with open(config_path) as f:
                return toml.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {"http":{"sources":[]}, "socks4":{"sources":[]}, "socks5":{"sources":[]}}
            
    def _get_protocol(self, source: str) -> str:
        """Determine proxy protocol for source"""
        if source in self.http_sources:
            return "http"
        elif source in self.socks4_sources:
            return "socks4" 
        elif source in self.socks5_sources:
            return "socks5"
        return ""
        
    def _parse_proxy(self, line: str, protocol: str) -> Optional[str]:
        """Parse and format proxy line"""
        proxy = line.strip()
        return f"{protocol}://{proxy}" if proxy else None
        
    async def _scrape_source(self, session: aiohttp.ClientSession, source: str) -> List[str]:
        """Scrape proxies from single source asynchronously"""
        try:
            async with session.get(source, timeout=self.timeout) as response:
                if response.status != 200:
                    logger.warning(f"Failed to scrape {source}: Status {response.status}")
                    return []
                    
                text = await response.text()
                protocol = self._get_protocol(source)
                proxies = []
                
                for line in text.splitlines():
                    if proxy := self._parse_proxy(line, protocol):
                        proxies.append(proxy)
                        
                logger.info(f"Scraped {len(proxies)} proxies from {source}")
                return proxies
                
        except Exception as e:
            logger.error(f"Error scraping {source}: {e}")
            return []
            
    async def _check_proxy(self, session: aiohttp.ClientSession, proxy: str) -> Optional[str]:
        """Verify if proxy is working"""
        try:
            async with session.get(
                "http://httpbin.org/ip", 
                proxy=proxy,
                timeout=self.timeout
            ) as response:
                if response.status == 200:
                    return proxy
        except Exception:
            pass
        return None
            
    async def scrape_proxies(self, source_limit: Optional[int] = 10) -> List[str]:
        """
        Scrape and verify proxies from multiple sources asynchronously
        Args:
            source_limit: Max number of sources to scrape from
        Returns:
            List of working formatted proxy addresses
        """
        logger.info("Starting async proxy scrape")
        sources = self.http_sources + self.socks4_sources + self.socks5_sources
        if source_limit:
            sources = sources[:source_limit]
            
        connector = aiohttp.TCPConnector(limit=None, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            # Scrape proxies concurrently
            scrape_tasks = [
                self._scrape_source(session, source) 
                for source in sources
            ]
            proxy_lists = await gather(*scrape_tasks)
            
            # Flatten proxy lists
            all_proxies = [
                proxy 
                for proxy_list in proxy_lists 
                for proxy in proxy_list
            ]
            
            logger.info(f"Found {len(all_proxies)} proxies, verifying...")
            
            # Verify proxies concurrently
            check_tasks = [
                self._check_proxy(session, proxy) 
                for proxy in all_proxies
            ]
            verified_proxies = await gather(*check_tasks)
            
            # Filter out None values (failed proxies)
            working_proxies = [p for p in verified_proxies if p]
            
            logger.info(f"Scraping complete - found {len(working_proxies)} working proxies")
            return working_proxies
            
def scrape_proxies(source_limit: Optional[int] = 10) -> List[str]:
    """Synchronous wrapper for async scraper"""
    return asyncio.run(AsyncProxyScraper().scrape_proxies(source_limit))