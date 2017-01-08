# nameclient.py
"""Vol 3B: Web Tech 1 (Internet Protocols). Solutions file."""


import requests
r = requests.get("http://localhost:8000?lastname=Hoppe")
r.close()
print r.headers
print r.content
