from fastapi import APIRouter, Response, status, Depends
from movies_api.models.movie import Movie
from movies_api.database import get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()

class MovieModel(BaseModel):
    id: int | None = None
    title: str

# Create movie
@router.post("/movies")
def movies_create(body: MovieModel):
    # TODO: create movie here
    return { 'data': body }

# List movies
class ListResponseBody(BaseModel):
    data: list[MovieModel]
@router.get("/movies")
def movies_list(limit: int | None = 10, offset: int | None = 0, db: Session = Depends(get_db)) -> ListResponseBody:
    data = db.query(Movie).offset(offset).limit(limit).all()
    return { 'data': data }

# Get movie
class GetResponseBody(BaseModel):
    data: MovieModel
@router.get("/movies/{id}")
def movies_get(id: int, db: Session = Depends(get_db)) -> GetResponseBody:
    data = db.query(Movie).filter(Movie.id == id).first()
    if not data:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return { 'data': data }

# Update movie
@router.put("/movies/{id}")
def movies_update(id: int, body: MovieModel):
    # TODO: update movie here
    # TODO: return 404 if movie doesn't exist
    # result = pg.update(playlist_model.TABLE_NAME, id, body.to_db())
    # if result.rowcount > 0:
    #     data = { **body.model_dump(), 'id': id }
    #     return { 'data': data }
    # else:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND)
    status_code = 404
    return Response(status_code=status_code)

# Delete movie
@router.delete("/movies/{id}")
def movies_delete(id: int):
    # TODO: delete movie here
    # result = pg.delete(playlist_model.TABLE_NAME, id)
    # status_code = status.HTTP_200_OK if result.rowcount > 0 else status.HTTP_404_NOT_FOUND
    status_code = 404
    return Response(status_code=status_code)
