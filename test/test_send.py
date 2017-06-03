import requests
import json

# This is test module as sender, to test send data to mongoq

# set headers
headers = {
    'Content-type' : 'application/json',
    'Accept' : 'text/plain'
}

# set data to be sent
data = {
    'content' :  {'init':1},
    'url' : 'http://127.0.0.1:3001/emit',
    'timeout' : 1
}

# set mongoq url
url = 'http://127.0.0.1:3000/caching'

# HTTP POST
requests.post(url, headers=headers, data=json.dumps(data))