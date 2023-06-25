"""two queries in 2 threads"""
import threading
import time

import requests

url = "https://httpbin.org/ip", "https://httpbin.org/headers"


def main(url: str) -> None:
    with requests.Session() as session:
        print(session.get(url).url)


start = time.monotonic()
thr1 = threading.Thread(target=main, args=(url[0],))
thr2 = threading.Thread(target=main, args=(url[1],))
lock = threading.Lock()
thr1.start()
thr2.start()
thr1.join()
print(time.monotonic() - start)
