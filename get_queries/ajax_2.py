import csv
from itertools import tee
import json
from pathlib import Path
import sqlite3
from typing import Any

from requests import Session
from tqdm import tqdm

domain = "https://edtechs.ru/"
url = "https://edtechs.ru/edtech_datatable/"
store = Path(__file__).parent.joinpath(f"{Path(__file__).stem}_data")

info = {
    "q_1_2019-q_2_2019": (1, 2),
    "q_3_2019-q_4_2019": (3, 4),
    "q_1_2020-q_2_2020": (5, 6),
    "q_3_2020-q_4_2020": (7, 8),
    "total_2020-total_2021": (9, 10),
    "q_1_2021-q_2_2021": (11, 28),
    "q_3_2021-q_4_2021": (29, 30),
    "q_1_2022-q_2_2022": (32, 33),
    "q_3_2022-q_4_2022": (34, 35),
    "total_2021-total_2022": (31, 36),
    "q_1_2023-q_1_2023": (37, 37),
}

columns = (
    "name",
    "activity",
    "foundation_year",
    "proceed_until",
    "proceed_from",
    "direction_names",
    "audience_names",
    "owners",
    "company_type_names",
)

columns_before = (
    "name",
    "activity",
    "foundation_year",
    "proceed_from",
    "direction_names",
    "audience_names",
    "owners",
    "company_type_names",
)

columns_after = (
    "name",
    "activity",
    "foundation_year",
    "proceed_until",
    "direction_names",
    "audience_names",
    "owners",
    "company_type_names",
)

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}


def get_companies_data(url: str, session: Session,
                       proceed_from: int, proceed_until: int) -> dict:
    params = {"proceed_from": proceed_from, "proceed_until": proceed_until}
    response = session.get(url, params=params)
    return response.json()


def save_json(name: str, data: dict) -> None:
    if not store.exists(): store.mkdir()
    with open(store.joinpath(f"{name}.json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def save_as_csv(data: tuple[list[dict], list[dict]], name: str) -> None:
    if not store.exists(): store.mkdir()
    name_before, name_after = name.split("-")
    before, after = data
    with open(store.joinpath(f"{name_before}.csv"), "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, columns_before, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(before)
    with open(store.joinpath(f"{name_after}.csv"), "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, columns_after, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(after)


def parse_json(json_object: Any) -> tuple[list[dict], list[dict]]:
    companies: list[dict[str, Any]] = json_object["data"]
    companies_before, companies_after = [], []
    for company in companies:
        main_data = ((key, value) for key, value in company.items() if key in columns)
        main_data = tee(map(lambda tpl: (tpl[0], tpl[1][0])
                        if tpl[0] == "proceed_until" else tpl, main_data))
        before = dict((key, value) for key, value in main_data[0] if key != "proceed_until")
        after = dict((key, value) for key, value in main_data[1] if key != "proceed_from")
        companies_before.append(before)
        companies_after.append(after)
    return companies_before, companies_after


def save_data_in_db() -> None:
    con = sqlite3.connect(store.joinpath(f"{Path(__file__).stem}_data.db"))
    for csv_file in store.iterdir():
        if csv_file.suffix == ".csv":
            con.execute(f"create table if not exists {csv_file.stem}(name text, "
                         "activity text, foundation_year int, revenue real, "
                         "direction_names text, audience_names text, owners text, "
                         "company_type_names text)")
            file = open(csv_file, encoding="utf-8")
            loaded = csv.reader(file)
            next(loaded)
            for line in loaded:
                con.execute(f"insert into {csv_file.stem} "
                             "values(?, ?, ?, ?, ?, ?, ?, ?)", line)
            file.close()
    con.commit()
    con.close()


def main() -> None:
    session = Session()
    session.headers.update(headers)
    for name, values in tqdm(info.items()):
        response = get_companies_data(url, session, *values)
        parsed_response = parse_json(response)
        save_as_csv(parsed_response, name)
    save_data_in_db()
    print(f"data has been saved in {store}")


if __name__ == "__main__":
    main()
