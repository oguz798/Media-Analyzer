import pytest

from media_analyzer.core import summarize_movies


def test_summarize_movies_full():
    movies_test_data_full = [
        {
            "title": "Inception",
            "year": 2010,
            "genres": ["Sci-Fi", "Thriller"],
            "watched": True,
            "size_gb": 8.5,
        },
        {
            "title": "Interstellar",
            "year": 2014,
            "genres": ["Sci-Fi"],
            "watched": False,
            "size_gb": 12.3,
        },
        {
            "title": "The Dark Knight",
            "year": 2008,
            "genres": ["Action"],
            "watched": True,
            "size_gb": 9.1,
        },
    ]

    summary = summarize_movies(movies_test_data_full)

    assert summary["total_movies"] == 3
    assert summary["total_size_gb"] == pytest.approx(29.9)
    assert summary["unwatched_count"] == 1
    assert summary["oldest_year"] == 2008


def test_summarize_movies_empty():

    summary = summarize_movies([])
    assert summary["total_movies"] == 0
    assert summary["total_size_gb"] == pytest.approx(0.0)
    assert summary["unwatched_count"] == 0
    assert summary["oldest_year"] is None
