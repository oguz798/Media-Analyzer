import argparse
import json
import pathlib
import sys

from media_analyzer.core import summarize_movies


def main() -> None:

    project_root = pathlib.Path(__file__).resolve().parent.parent.parent
    default_path = project_root / "sample_data" / "movies.json"

    parser = argparse.ArgumentParser(description="Analyze a movie library JSON file.")
    parser.add_argument("file", nargs="?", help="Path to JSON file")

    args = parser.parse_args()

    if args.file:
        data_path = pathlib.Path(args.file)
    else:
        data_path = default_path

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


if __name__ == "__main__":
    main()
