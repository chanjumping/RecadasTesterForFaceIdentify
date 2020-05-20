import requests
import json

headers = {'Content-type': 'application/json'}

r = requests.post(url="http://172.16.148.33:8888/heartBeat.do", headers=headers)

print(r.text)