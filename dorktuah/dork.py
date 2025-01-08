from .modules.engine import Engine

def dork(query, use_proxy:bool=True, use_custom:bool=True):
    google = Engine(use_proxy=use_proxy, use_custom=use_custom)
    results = google.search(query)
    return results