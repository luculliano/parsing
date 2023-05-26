import requests
from tqdm import tqdm

url_media = "https://stream.voidboost.cc/7ee43645fc7e49efa398d854e96236eb:2023052713:a294S2ROUkVZUzVDWE1kTlVROUhxQ2MyTnpNa0l6V1ZGeE44VTZMaFc4R1JJd0R4TXJqRW9wS3RjUm9SN0xUQThtczJueGlBUHhRRmNBR1hnekI0M3c9PQ==/7/5/7/9/0/7/elvt5.mp4"

url_page = "https://rezka.ag/films/crime/1237-lico-so-shramom-1983.html"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}


def dowlnload_media(url: str) -> None:
    response = requests.get(url, headers=headers, stream=True)
    with open("scareface.mp4", "wb") as file:
        for chunk in tqdm(response.iter_content(10362880), desc="downloading..."):
            file.write(chunk)


def get_media(url: str) -> None:
    response = requests.get(url, headers=headers)
    with open("index.html", "w") as file:
        print(response.content.decode(), file=file)


if __name__ == "__main__":
    get_media(url_page)
