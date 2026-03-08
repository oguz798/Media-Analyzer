import argparse
import json
import pathlib
import sys
import os
import requests

from media_analyzer.core import summarize_movies
from media_analyzer.radarr import fetch_radarr_movies


def main() -> None:

    project_root = pathlib.Path(__file__).resolve().parent.parent.parent
    default_path = project_root / "sample_data"

    parser = argparse.ArgumentParser(description="Analyze a movie library JSON file.")
    parser.add_argument("file", nargs="?", help="Path to JSON file")
    parser.add_argument(
        "--source",
        "-s",
        default="json",
        choices=["json", "radarr"],
        help="Data source to analyze (json or radarr)",
    )
    args = parser.parse_args()

    if args.file:
        data_path = pathlib.Path(args.file)
    else:
        data_path = default_path
    if args.source == "json":
        try:
            with data_path.open(encoding="utf-8") as f:
                movies = json.load(f)
                summary = summarize_movies(movies)
                print(f"Total movies: {summary['total_movies']}")
                print(f"Total size (GB): {summary['total_size_gb']}")
                print(f"Unwatched: {summary['unwatched_count']}")
                oldest_year = summary["oldest_year"]
                oldest_display = oldest_year if oldest_year is not None else "N/A"
                print(f"Oldest year: {oldest_display}")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: file not found or invalid JSON.")
            sys.exit(1)
    elif args.source == "radarr":
        radarr_url = os.getenv("RADARR_URL")
        radarr_api_key = os.getenv("RADARR_API_KEY")

        print("Radarr URL:", radarr_url)
        print("API key loaded:", bool(radarr_api_key))

        if not radarr_url or not radarr_api_key:
            print("Missing either radarr url or api key")
            sys.exit(1)

        normalized_movies = fetch_radarr_movies(radarr_url, radarr_api_key)
        summary = summarize_movies(normalized_movies)
        print(f"Total movies: {summary['total_movies']}")
        print(f"Total size (GB): {summary['total_size_gb']}")
        print(f"Unwatched: {summary['unwatched_count']}")
        oldest_year = summary["oldest_year"]
        oldest_display = oldest_year if oldest_year is not None else "N/A"
        print(f"Oldest Movie: {oldest_display}")


if __name__ == "__main__":
    main()
