from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional
from movies_api.models.base import Base

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100), index=True)

    plot: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    director: Mapped[Optional[str]]

    year: Mapped[Optional[int]]
    runtime: Mapped[Optional[int]]
    imdb_rating: Mapped[Optional[float]]

    writer: Mapped[Optional[str]]
    genre: Mapped[Optional[str]]
    actors: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r}"
