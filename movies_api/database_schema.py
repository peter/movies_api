from movies_api.database import engine
from movies_api.models.movie import Movie

def init_db_schema():
    Movie.metadata.create_all(engine)
