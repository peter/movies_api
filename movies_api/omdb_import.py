import json
import traceback
import movies_api.services.omdb as omdb
from movies_api.database import engine, db_connect
from movies_api.database_schema import init_db_schema
from movies_api.models.movie import Movie
from sqlalchemy.orm import Session

MOVIE_TITLES_FILE_PATH = 'data/imdb-top-250-movie-titles.txt'

def read_movie_titles():
    with open(MOVIE_TITLES_FILE_PATH) as file:
        lines = [line.rstrip() for line in file]
        return lines

def save_movie(movie, session):
    try:
        db_movie = Movie(**movie)
        session.add_all([db_movie])
        session.commit()
        return True
    except Exception as error:
        print(f'Error thrown saving movie in db', movie, error, traceback.format_exc())
        return False

def import_movies(movie_titles, session):
    movies = []
    for index, movie_title in enumerate(movie_titles):
        print(f'Downloading movie {index + 1}/{len(movie_titles)}: {movie_title}')
        movie = omdb.get_movie_by_title(movie_title)
        if movie:
            if save_movie(movie, session):
                movies.append(movie)
        else:
            print(f'Could not find movie {movie_title}')
    return movies

def run_import():
    db_connect()
    init_db_schema()
    with Session(engine) as session:
        movie_titles = read_movie_titles()
        movies = import_movies(movie_titles, session)
        print(f'Number of movies imported: {len(movies)} / {len(movie_titles)}')
        print(json.dumps(movies, indent=2))
