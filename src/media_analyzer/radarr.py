import requests
from media_analyzer.models import Movie


def fetch_radarr_movies(radarr_url: str, api_key: str) -> list[Movie]:
    headers = {"X-Api-Key": api_key}
    movie_url = radarr_url + "/api/v3/movie"
    response = requests.get(movie_url, headers=headers)
    response.raise_for_status()
    movie_data = response.json()
    # file_path = default_path / "movie_data.json"
    # with open(file_path, "w") as json_file:
    #    json.dump(movie_data, json_file, indent=4)
    # print("Radarr status code:", response.status_code)
    # print(movie_data[0])

    normalized_movies = []

    for movie in movie_data:
        size_bytes = movie.get("sizeOnDisk", 0)
        size_gb = size_bytes / (1024**3)
        normalized_movie = Movie(
            title=movie["title"],
            year=movie["year"],
            size_gb=size_gb,
            watched=False,
        )

        normalized_movies.append(normalized_movie)
    return normalized_movies
