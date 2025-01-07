from modules import Google

# query = 'insite:"youtube.com" "WINDOWS10XPRO"'
query = "how to bake a cake"
google = Google(use_proxy=False)
results = google.search(query)
print(results)