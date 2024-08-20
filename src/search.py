from vector_store import search_by_text, find_recommendations, scroll

from titles import get_formatted_title, find_by_title_id


def search():
    model = {"name": "bge-small-en-v1.5", "size": 384}
    collection_name = f"title_{model["name"].replace("-", "_")}"

    # The Shawshank Redemption
    # title = find_by_title_id(278)
    # results = search_by_text(collection_name, get_formatted_title(title), 5)
    results = find_recommendations(collection_name, [278, 238, 240, 424], [122])
    for result in results:
        # print(result)
        print(result.payload["name"], result.payload["vote_average"])


def recommend():
    model = {"name": "bge-small-en-v1.5", "size": 384}
    collection_name = f"title_{model["name"].replace("-", "_")}"
    likes = []
    dislikes = []
    not_watched = []
    recommendations = []
    while True:
        if len(likes) >= 10:
            recommended_title = True
            results = find_recommendations(
                collection_name, likes, dislikes, not_watched, limit=1
            )
        else:
            recommended_title = False
            results = scroll(collection_name, likes, dislikes, not_watched, limit=10)
        for result in results:
            print(result.payload["name"])
            print(f"IMDB Rating: {result.payload['vote_average']}")
            print("\n\n")
            print(result.payload.get("overview"))
            print(
                "Enter 1 for like, 2 for dislike, 3 for not watched, or 4 to show all recommendations."
            )
            while True:
                choice_str = input("> ")
                choice = 0
                if choice_str.isnumeric():
                    choice = int(choice_str)
                if choice == 0 or choice > 4:
                    print("Invalid choice. Allowed options are 1, 2 and 3.")
                else:
                    break
            if choice == 1:
                likes.append(result.id)
            elif choice == 2:
                dislikes.append(result.id)
            elif choice == 3:
                not_watched.append(result.id)
                if recommended_title:
                    recommendations.append(
                        {
                            "id": result.id,
                            "name": result.payload["name"],
                            "rating": result.payload["vote_average"],
                        }
                    )
            elif choice == 4:
                for recommendation in recommendations:
                    print(
                        recommendation["id"],
                        recommendation["name"],
                        recommendation["rating"],
                    )


if __name__ == "__main__":
    recommend()
