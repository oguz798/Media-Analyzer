def summarize_movies(movies: list[dict]) -> dict:
    """
    Return a summary dict with:
      - total_movies (int)
      - total_size_gb (float)
      - unwatched_count (int)
      - oldest_year (int | None)  # None if list empty
    """
    summary = {
        "total_movies": 0,
        "total_size_gb": 0.0,
        "unwatched_count": 0,
        "oldest_year": None,
    }

    if not movies:
        return summary

    oldest_year = None
    for movie in movies:
        
        summary["total_movies"] += 1
        summary["total_size_gb"] += movie["size_gb"]
        if not movie["watched"]:
            summary["unwatched_count"] += 1
        if oldest_year is None:
            oldest_year = movie["year"]
        else:
            oldest_year = min(movie["year"], oldest_year)
    summary["oldest_year"] = oldest_year
    return summary
