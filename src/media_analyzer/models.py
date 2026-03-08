from dataclasses import dataclass


@dataclass
class Movie:
    title: str
    year: int
    size_gb: float
    watched: bool
