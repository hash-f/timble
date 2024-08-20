import json

_titles = []


def load_titles_from_disk():
    global _titles
    if len(_titles) > 0:
        return _titles

    file_path = "./data/top-titles.jsonl"
    with open(file_path, "r") as fh:
        for line in fh:
            title = json.loads(line)
            _titles.append(title)

    return _titles


def find_by_title_id(title_id):
    titles = load_titles_from_disk()
    return next(title for title in titles if title["id"] == title_id)


def get_restructured_titles(titles):
    docs = []
    metadata = []
    ids = []
    for title in titles:
        if title.get("title") and title.get("overview"):
            docs.append(get_formatted_title(title))
            metadata.append(get_metadata_from_title(title))
            ids.append(title["id"])
    return docs, metadata, ids


def get_formatted_title(title):
    return json.dumps(
        {
            "name": title.get("title"),
            "type": title.get("type"),
            "overview": title.get("overview"),
        }
    )


def get_metadata_from_title(title):
    return {
        "name": title.get("title"),
        "type": title.get("type"),
        "vote_average": title.get("vote_average"),
        "vote_count": title.get("vote_count"),
    }


if __name__ == "__main__":
    titles = load_titles_from_disk()
    print(len(titles))
