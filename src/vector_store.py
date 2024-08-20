from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    Range,
    VectorParams,
    RecommendStrategy,
    HasIdCondition,
    OrderBy,
)

_client = None


def get_client():
    global _client
    if _client is not None:
        return _client

    _client = QdrantClient(path="./db")
    # _client = QdrantClient(url="http://localhost:6333/")

    return _client


def create_collection(
    collection_name, size, distance=Distance.COSINE, delete_if_exists=False
):
    client = get_client()
    if delete_if_exists and client.collection_exists(collection_name):
        client.delete_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=size, distance=distance),
    )


def embed_documents(collection_name, docs, metadata, ids):
    client = get_client()
    client.add(
        collection_name=collection_name, documents=docs, metadata=metadata, ids=ids
    )


def search_by_text(collection_name, query_text, limit):
    client = get_client()
    return client.query(
        collection_name,
        query_text,
        query_filter=Filter(
            must=[FieldCondition(key="vote_average", range=Range(gte=7))]
        ),
        limit=limit,
    )


def scroll(collection_name, positive_ids=[], negative_ids=[], ignore_ids=[], limit=10):
    client = get_client()
    return client.scroll(
        collection_name=collection_name,
        order_by=OrderBy(
            key="vote_average",
            direction="desc",
        ),
        scroll_filter=Filter(
            must_not=[
                HasIdCondition(has_id=positive_ids + negative_ids + ignore_ids),
            ],
        ),
        limit=10,
    )[0]


def find_recommendations(
    collection_name, positive_ids=[], negative_ids=[], ignore_ids=[], limit=10
):
    client = get_client()

    return client.recommend(
        collection_name=collection_name,
        positive=positive_ids,
        negative=negative_ids,
        query_filter=Filter(
            must=[FieldCondition(key="vote_average", range=Range(gte=8))],
            must_not=[
                HasIdCondition(has_id=positive_ids + negative_ids + ignore_ids),
            ],
        ),
        strategy=RecommendStrategy.AVERAGE_VECTOR,
        using="fast-bge-small-en",
        limit=limit,
    )


def delete_collection(collection_name):
    client = get_client()
    client.delete_collection(collection_name)
