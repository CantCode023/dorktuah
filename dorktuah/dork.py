from .modules.engine import Engine

def dork(query, use_proxy:bool=True, use_custom:bool=True):
    engine = Engine(use_proxy=use_proxy, use_custom=use_custom)
    results = engine.search(query)
    return results