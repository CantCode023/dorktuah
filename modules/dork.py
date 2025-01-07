from . import Google
# from . import Bing
# from . import DuckDuckGo

def dorktuah(query, use_proxy, use_custom):
    google = Google(use_proxy=use_proxy, use_custom=use_custom)
    # bing = Bing()
    results = []
    results.append(google.search(query))
    # results.append(bing.search(query))