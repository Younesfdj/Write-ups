#!/usr/bin/env python3

import requests
import time 
uuid = "1d0163a3-c550-4974-abb1-6a014112c360"

headers = {
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Opera";v="117"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "Referer": "https://numberchamp-challenge.utctf.live/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

while (True) :
    url = f"https://numberchamp-challenge.utctf.live/match?uuid={uuid}&lat=36.7296512&lon=4.0271872"

    response = requests.post(url, headers=headers, data=None)
    data = response.json() 
    uuid = data["uuid"]
    if data["user"] == "geopy" : break
    time.sleep(1)


print(data)
