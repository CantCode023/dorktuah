# TODOLIST:

- [x] set up project structure
- [x] write proxy rotation implementation
  - proxy_pool as function
  - requests.get(proxies=ProxyPool()) for easier rotation
  - ProxyPool()
    - type:Literal["socks4", "socks5", "http", "all"] = "all"
    - get proxies from proxies.txt
  - [x] write a proxy checker to make sure the returned proxy is alive
- [x] write engine implementation
  - use BeautifulSoup
  - Engine()
    - site:str = "https://google.com"
    - num:int = 10 -> Number of results to return
    - start:int = 0 -> The index of result to start with
    - end:int = 10 -> The index of result to stop with
- [x] write etools scraping implementaiton

# FUTURE TODOLIST:

- [x] add scrape proxies and check proxies to ProxyPool to get newest proxies
- [ ] make proxy checker faster