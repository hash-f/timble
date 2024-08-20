import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_titles_for_page(title_type, page):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('TMDB_TOKEN')}",
    }

    url = f"https://api.themoviedb.org/3/{title_type}/top_rated?language=en-US&page={page}"
    response = requests.get(url, headers=headers)
    response_text = response.text
    response_json = json.loads(response_text)
    return {
        "titles": response_json["results"],
        "total_pages": response_json["total_pages"],
    }


def fetch_top_rated_titles(title_type):
    titles = []
    page = 1
    total_pages = 1
    while page <= total_pages:
        print(f"Sending request for page {page}")
        response = fetch_titles_for_page(title_type, page)
        if len(response["titles"]) != 0:
            titles.extend(response["titles"])
            total_pages = response["total_pages"]
            print(
                f"Found {len(response['titles'])} on page {page}, total pages {total_pages}"
            )
            with open("data/top-titles.jsonl", "a") as fh:
                for title in response["titles"]:
                    title["type"] = title_type
                    json.dump(title, fh)
                    fh.write("\n")
            page += 1
            time.sleep(0.1)


if __name__ == "__main__":
    fetch_top_rated_titles(title_type="movie")
    fetch_top_rated_titles(title_type="tv")
