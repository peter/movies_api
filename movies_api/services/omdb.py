import os
import requests
import traceback
import re

OMDB_API_URL = 'http://www.omdbapi.com'
OMDB_API_KEY = os.environ.get('OMDB_API_KEY')

def parse_year(year: str) -> int | None:
    # Example values: "2022", "2011–2013"
    m = re.match("^(\d\d\d\d)", year or '')
    return int(m.group(1)) if m else None

def parse_runtime(runtime: str) -> int:
    # Example value: "108 min"
    m = re.match("^(\d+)", runtime or '')
    return int(m.group(1)) if m else None

def parse_imdb_rating(imdb_rating: str) -> int | None:
    return float(imdb_rating) if imdb_rating else None

def to_movie_fields(omdb_fields):
    result = {
        'title': omdb_fields.get('Title'),
        'plot': omdb_fields.get('Plot'),
        'language': omdb_fields.get('Language'),
        'country': omdb_fields.get('Country'),
        'director': omdb_fields.get('Director'),

        'year': parse_year(omdb_fields.get('Year')),
        'runtime': parse_runtime(omdb_fields.get('Runtime')),
        'imdb_rating': parse_imdb_rating(omdb_fields.get('imdbRating')),

        # TODO: the following fields are comma separated strings that could be parsed to lists
        'writer': omdb_fields.get('Writer'),
        'genre': omdb_fields.get('Genre'),
        'actors': omdb_fields.get('Actors'),
    }

    return result

def get_movie_by_title(title):
    if not OMDB_API_KEY:
        raise Exception('You need to set env var OMDB_API_KEY to invoke the OMDB API')
    try:
        params = {
            'apiKey': OMDB_API_KEY,
            't': title
        }
        response = requests.get(OMDB_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'Error' in data:
                # NOTE: not found movies yield status 200 and {"Response":"False","Error":"Movie not found!"}
                return None
            return to_movie_fields(data)
        else:
            return None
    except Exception as error:
        print(f'Error thrown invoking OMDB API', params, error, traceback.format_exc())
        return None
