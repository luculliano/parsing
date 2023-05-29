"""query to onion site"""
import requests

url = "http://flibustaongezhld6dibs2dps6vm4nvqg2kp7vgowbu76tzopgnhazqd.onion/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
}

proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}


def get_query() -> None:
    response = requests.get(url, proxies=proxies, headers=headers)
    print(response.status_code)


if __name__ == "__main__":
    get_query()
