from modules.engines import Google
# from . import Bing
# from . import DuckDuckGo

def dork(query, use_proxy, use_custom):
    google = Google(use_proxy=use_proxy, use_custom=use_custom)
    # bing = Bing()
    results = []
    results.append(google.search(query))
    # results.append(bing.search(query))