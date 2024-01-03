from fastapi import APIRouter, Response, status, Depends
from movies_api.models.movie import Movie
from movies_api.database import get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()

class MovieModel(BaseModel):
    id: int | None = None
    title: str

READ_ONLY_FIELDS = ['id']

#######################################
# Helper Methods
#######################################

def writable_fields(body):
    body_dict = body.model_dump()
    return {k: body_dict[k] for k in body_dict.keys() if k not in READ_ONLY_FIELDS}

#######################################
# Endpoints
#######################################

# List movies
class ListResponseBody(BaseModel):
    data: list[MovieModel]
@router.get("/movies")
def movies_list(
    limit: int | None = 10,
    offset: int | None = 0,
    title: str | None = None,
    db: Session = Depends(get_db)
) -> ListResponseBody:
    query = db.query(Movie)
    if title:
        query = query.filter_by(title=title)
    data = query.order_by(Movie.title).offset(offset).limit(limit).all()
    return { 'data': data }

# Get movie
@router.get("/movies/{id}")
def movies_get(id: int, db: Session = Depends(get_db)) -> MovieModel:
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return movie

# Create movie
@router.post("/movies")
def movies_create(body: MovieModel, db: Session = Depends(get_db)) -> MovieModel:
    create_fields = writable_fields(body)
    movie = Movie(**create_fields)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

# Update movie
@router.put("/movies/{id}")
def movies_update(id: int, body: MovieModel, db: Session = Depends(get_db)) -> MovieModel:
    movie = db.query(Movie).filter(Movie.id==id).first()
    if not movie:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    update_fields = writable_fields(body)
    for field, value in update_fields.items():
        setattr(movie, field, value)
    db.commit()
    db.refresh(movie)
    return movie

# Delete movie
@router.delete("/movies/{id}")
def movies_delete(id: int, db: Session = Depends(get_db)):
    # TODO: delete without fetching the movie would be more efficient
    movie = db.query(Movie).filter(Movie.id==id).first()
    if not movie:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(movie)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
