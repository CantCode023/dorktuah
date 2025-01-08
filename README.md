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
    - proxy_pool implementation
- [x] write etools scraping implementaiton
- [ ] implement proxy pool in engine.py

# FUTURE TODOLIST:

- [x] add scrape proxies and check proxies to ProxyPool to get newest proxies
- [ ] make proxy checker faster