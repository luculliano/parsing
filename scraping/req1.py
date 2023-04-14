import json
import os
import sys
from time import monotonic

import requests

###############################################################################
# request json get
# res = requests.get("https://api.covidtracking.com/v1/us/current.json")
# json.dump(*res.json(), fp=sys.stdout, indent=2)

###############################################################################
# using params for API
# api_key = os.getenv("OWM_API")
# url = "https://api.openweathermap.org/data/2.5/weather"
# params = {"appid": api_key, "lat": 44.34, "lon": 10.99}
# res = requests.get(url=url, params=params)
# print(res.url)
###############################################################################
# download file
# url = "https://httpbin.org/image/jpeg"
# res = requests.get(url=url)
# with open(f"downloaded.jpeg", "wb") as file:
#     file.write(res.content)

# download large file
# url = "https://user-images.githubusercontent.com/1991296/224442907-7693d4be-acaa-4e01-8b4f-add84093ffff.mp4"
# res = requests.get(url=url, stream=True)
# with open("video.mp4", "wb") as file:
#     for chunk in res.iter_content(chunk_size=1_000_000):
#         if chunk:
#             file.write(chunk)
###############################################################################
# using proxy
# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"}
# proxy = {"http": "http://72bb24:ed1aea@87.251.76.222:1010", "https": "http://72bb24:ed1aea@87.251.76.222:1010"}
# url = "https://httpbin.org/user-agent"
# res = requests.get("https://ipinfo.io/json",  proxies=proxy, headers=headers)
# print(res.text)
###############################################################################
