from fastapi import APIRouter, Response, status, Depends
from movies_api.models.movie import Movie
from movies_api.database import get_db
import movies_api.services.omdb as omdb
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()

class MovieModel(BaseModel):
    id: int | None = None

    title: str

    plot: str | None = None
    language: str | None = None
    country: str | None = None
    director: str | None = None

    year: int | None = None
    runtime: int | None = None
    imdb_rating: float | None = None

    writer: str | None = None
    genre: str | None = None
    actors: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

READ_ONLY_FIELDS = ['id', 'created_at', 'updated_at']

#######################################
# Helper Methods
#######################################

def writable_fields(fields):
    return {k: fields[k] for k in fields.keys() if k not in READ_ONLY_FIELDS}

def create_movie(db, create_fields):
    movie = Movie(**create_fields)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

#######################################
# Endpoints
#######################################

# List movies endpoint
class ListResponseBody(BaseModel):
    data: list[MovieModel]
    count: int
    limit: int
    offset: int
@router.get("/movies", response_model_exclude_none=True)
def movies_list(
    limit: int | None = 10,
    offset: int | None = 0,
    title: str | None = None,
    db: Session = Depends(get_db)
) -> ListResponseBody:
    count = db.query(Movie).count()
    query = db.query(Movie)
    if title:
        query = query.filter_by(title=title)
    movies = query.order_by(Movie.title).offset(offset).limit(limit).all()
    return {
        'data': movies,
        'count': count,
        'limit': limit,
        'offset': offset
    }

# Get movie endpoint
@router.get("/movies/{id}", response_model_exclude_none=True)
def movies_get(id: int, db: Session = Depends(get_db)) -> MovieModel:
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return movie

# Add movie from OMDB endpoint
class OMDBQueryModel(BaseModel):
    title: str
@router.post("/movies/omdb-add", response_model_exclude_none=True)
def movies_omdb_add(body: OMDBQueryModel, db: Session = Depends(get_db)) -> MovieModel:
    omdb_movie = omdb.get_movie_by_title(body.title)
    if not omdb_movie:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    create_fields = writable_fields(omdb_movie)
    movie = create_movie(db, create_fields)
    return movie

# Create movie endpoint
@router.post("/movies", response_model_exclude_none=True)
def movies_create(body: MovieModel, db: Session = Depends(get_db)) -> MovieModel:
    create_fields = writable_fields(body.model_dump())
    movie = create_movie(db, create_fields)
    return movie

# Update movie endpoint
@router.put("/movies/{id}", response_model_exclude_none=True)
def movies_update(id: int, body: MovieModel, db: Session = Depends(get_db)) -> MovieModel:
    movie = db.query(Movie).filter(Movie.id==id).first()
    if not movie:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    update_fields = writable_fields(body.model_dump())
    update_fields['updated_at'] = datetime.now()
    for field, value in update_fields.items():
        setattr(movie, field, value)
    db.commit()
    db.refresh(movie)
    return movie

# Delete movie endpoint
@router.delete("/movies/{id}")
def movies_delete(id: int, db: Session = Depends(get_db)):
    # TODO: delete without fetching the movie would be more efficient
    movie = db.query(Movie).filter(Movie.id==id).first()
    if not movie:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(movie)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
