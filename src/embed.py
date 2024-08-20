from titles import load_titles_from_disk, get_restructured_titles
from vector_store import embed_documents, create_collection


def embed_titles():
    titles = load_titles_from_disk()
    docs, metadata, ids = get_restructured_titles(titles)
    model = {"name": "bge-small-en-v1.5", "size": 384}
    collection_name = f"title_{model["name"].replace("-", "_")}"
    # create_collection(collection_name, model["size"])
    embed_documents(collection_name, docs, metadata, ids)


if __name__ == "__main__":
    embed_titles()
