import csv
import json

import requests


def get_edu() -> None:
    url = "https://edtechs.ru/edtech_datatable/?"
    params = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }
    response = requests.get(url, params=params)
    with open("edu.json", "w") as file:
        json.dump(response.json(), file, indent=3, ensure_ascii=False)


def parse_edu() -> None:
    with open("edu.json") as file:
        loaded = json.load(file)
        data = sorted(loaded["data"], key=lambda dct: dct["rating"])
    with open("edu.csv", "w") as file:
        headers = [
            "id",
            "name",
            "logo__file",
            "activity",
            "client__type",
            "foundation_year",
            "proceed_until",
            "proceed_from",
            "proceed_is_rating",
            "direction_names",
            "audience_names",
            "owners",
            "founders",
            "owner",
            "owner_photo",
            "company_type_names",
            "rating",
            "last_rating",
        ]
        writer = csv.DictWriter(file, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(data)
