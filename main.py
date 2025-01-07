# Will add dorking later
from modules import dorktuah

query = 'insite:"youtube.com" "WINDOWS10XPRO"'
results = dorktuah(query, use_proxy=False, use_custom=True)
print(results)