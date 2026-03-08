import argparse
import json
import os
import pathlib
import sys

from media_analyzer.core import largest_movies, summarize_movies, get_unwatched_movies
from media_analyzer.radarr import fetch_radarr_movies
from media_analyzer.sources import load_json_movies


def main() -> None:

    project_root = pathlib.Path(__file__).resolve().parent.parent.parent
    default_path = project_root / "sample_data" / "movies.json"

    parser = argparse.ArgumentParser(description="Analyze a movie library JSON file.")
    parser.add_argument("file", nargs="?", help="Path to JSON file")
    parser.add_argument(
        "--source",
        "-s",
        default="json",
        choices=["json", "radarr"],
        help="Data source to analyze (json or radarr)",
    )
    parser.add_argument(
        "--largest",
        type=int,
        metavar="N",
        help="Show the largest N movies by size (GB)",
    )
    parser.add_argument(
        "--unwatched",
        action="store_true",
        help="List unwatched movies",
    )
    args = parser.parse_args()

    if args.file:
        data_path = pathlib.Path(args.file)
    else:
        data_path = default_path
    if args.source == "json":
        movies = load_json_movies(data_path)
    elif args.source == "radarr":
        radarr_url = os.getenv("RADARR_URL")
        radarr_api_key = os.getenv("RADARR_API_KEY")

        if not radarr_url or not radarr_api_key:
            print("Missing either radarr url or api key")
            sys.exit(1)

        movies = fetch_radarr_movies(radarr_url, radarr_api_key)

    if args.largest is not None:
        top_movies = largest_movies(movies, args.largest)
        print(f"Top {args.largest} largest movies:")

        for idx, movie in enumerate(top_movies, start=1):
            print(f"{idx}. {movie.title} ({movie.year}) - {movie.size_gb:.2f} GB")

    elif args.unwatched is not None:
        unwatched_movies = get_unwatched_movies(movies)
        print("Unwatched movies:")

        for idx, movie in enumerate(unwatched_movies, start=1):
            print(f"{idx}. {movie.title} ({movie.year}) - {movie.size_gb:.2f} GB")

    else:
        summary = summarize_movies(movies)
        print(f"Total movies: {summary['total_movies']}")
        print(f"Total size (GB): {summary['total_size_gb']}")
        print(f"Unwatched: {summary['unwatched_count']}")
        oldest_year = summary["oldest_year"]
        oldest_display = oldest_year if oldest_year is not None else "N/A"
        print(f"Oldest Movie: {oldest_display}")


if __name__ == "__main__":
    main()
