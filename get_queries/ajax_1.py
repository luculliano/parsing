import requests

# determine url, using own data: https://bitality.cc/Home/Index/BTC--APE
# check resonse headers there is: "X-Requested-With": "XMLHttpRequest"
# open Network -> XHR -> find link: https://bitality.cc/Home/GetSum?GiveName=Bitcoin&GetName=ApeCoin&Sum=0.13705695&Direction=0
# check response tab

# P.S. can't extract cookies cause it's cloudflare protection

domain = "https://bitality.cc/"
url = "https://bitality.cc/Home/GetSum"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "x-requested-with": "XMLHttpRequest",
    "Accept": "*/*",
    "Cookie": "cf_clearance=TCYLivdY7nQI_J5SvNf0A8PU56Vnwhi9tKdi5OA7S4o-1684858581-0-150; .Session=CfDJ8AhTwXAHybxHrD7AGEqjNRfX1OvsVE%2Fa8sCZ9lkm3xCvotY2snQRNhakrHtUNAIAcvWAIKJ9O%2FOZwWAaxNksfmiBfRWjodJvIfOBCbvd%2BMEQKldvIEjdtTnvFvgXJKdGSG8H5mLCleXgmY3BdbPJvhEa3uvUER88MUmvFYc6gVmx; RefererSite=https%3A%2F%2Fbitality.cc%2F",
}

params = {"GiveName": "Bitcoin", "GetName": "ApeCoin", "Sum": 0.2, "Direction": 0}


def get_btc(url: str) -> None:
    with requests.get(url, headers=headers, params=params) as response:
        print(response.json(), response.headers)


def get_cookies(url: str) -> None:
    with requests.get(url, headers=headers) as response:
        print(response.headers)


if __name__ == "__main__":
    get_btc(url)
    get_cookies(domain)
