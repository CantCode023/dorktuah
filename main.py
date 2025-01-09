import dorktuah

query = 'site:"youtube.com" "WINDOWS10XPRO"'
results = dorktuah.dork(
    query=query,
    proxy_type="all",
    use_proxy=True,
    use_custom=True,
    proxy_path="path_to_proxy",
    source_limit=10
)
print(results)