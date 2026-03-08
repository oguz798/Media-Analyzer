import pathlib
import json
import sys
from media_analyzer.models import Movie


def load_json_movies(data_path: pathlib.Path) -> list[Movie]:
    try:
        with data_path.open(encoding="utf-8") as f:
            data = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: file not found or invalid JSON.")
        sys.exit(1)

    movies = []

    for item in data:
        movie = Movie(
            title=item.get("title"),
            year=item.get("year"),
            size_gb=item.get("size_gb", 0),
            watched=item.get("watched", False),
        )

        movies.append(movie)

    return movies
