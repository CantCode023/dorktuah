# Will add dorking later
import dorktuah

query = 'site:"youtube.com" "WINDOWS10XPRO"'
results = dorktuah.dork(query, use_proxy=False, use_custom=True)
print(results)