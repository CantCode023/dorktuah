![Header](./assets/header.png)

# About

Dorktuah is a powerful Python library designed for advanced Google dorking and web scraping through proxy rotation. It leverages multiple search engines while maintaining anonymity through an extensive proxy system. The project aims to provide researchers, security professionals, and developers with a reliable tool for gathering information while avoiding rate limiting and IP blocks.

Key features:
- Automated proxy rotation system
- Support for multiple proxy types (HTTP, SOCKS4, SOCKS5)
- Built-in proxy scraper with 100+ sources
- Proxy health checking and validation
- Clean and structured search results
- Rate limit avoidance through proxy rotation
- Custom proxy list support

The name "Dorktuah" combines "dork" (referring to Google dorking) with "tuah" (meaning luck/fortune in Malay), signifying a fortunate/successful dorking tool.

---

# Installation

To install Dorktuah, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/CantCode023/dorktuah.git
```

2. Navigate to the project directory:
```bash
cd dorktuah
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

---

# Examples

Here are several examples demonstrating how to use Dorktuah:

### Basic Search
```python
import dorktuah

# Simple search query
results = dorktuah.dork('site:"example.com" filetype:pdf')
print(results)
```

### Using Specific Proxy Type
```python
import dorktuah

# Search using only SOCKS5 proxies
results = dorktuah.dork(
    'site:"github.com" "password"',
    proxy_type="socks5",
    use_proxy=True
)
print(results)
```

### Using Custom Proxy List
```python
import dorktuah

# Use custom proxy list from specific path
results = dorktuah.dork(
    'intext:"confidential" site:"company.com"',
    use_proxy=True,
    use_custom=True,
    proxy_path="path/to/proxies.txt"
)
print(results)
```

### Advanced Search with Limited Sources
```python
import dorktuah

# Limit proxy sources and use HTTP proxies
results = dorktuah.dork(
    'intitle:"index of" intext:"parent directory"',
    proxy_type="http",
    use_proxy=True,
    use_custom=False,
    source_limit=5
)
print(results)
```

The results are returned in a structured format:
```python
[
    {
        "url": "https://example.com/page",
        "title": "Page Title",
        "description": "Page description from search results"
    },
    # ... more results
]
```

### Best Practices

1. Always start with a smaller `source_limit` when testing:
```python
results = dorktuah.dork(query, source_limit=5)
```

2. Use specific proxy types for better reliability:
```python
results = dorktuah.dork(query, proxy_type="socks5")
```

3. Implement error handling:
```python
try:
    results = dorktuah.dork(query)
except Exception as e:
    print(f"Error occurred: {e}")
```

4. Consider using custom proxy lists for consistent performance:
```python
results = dorktuah.dork(query, use_custom=True, proxy_path="reliable_proxies.txt")
```

The library automatically handles:
- Proxy rotation
- Health checks
- Rate limiting avoidance
- Result parsing and formatting

Remember to use this tool responsibly and in accordance with the target website's terms of service and applicable laws.

---

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
- [x] implement proxy pool in engine.py

---

# FUTURE TODOLIST:

- [x] add scrape proxies and check proxies to ProxyPool to get newest proxies
- [ ] make proxy checker faster