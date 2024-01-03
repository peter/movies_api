import os
import requests
import traceback

OMDB_API_URL = 'http://www.omdbapi.com'
OMDB_API_KEY = os.environ.get('OMDB_API_KEY')

def get_movie_by_title(title):
    try:
        params = {
            'apiKey': OMDB_API_KEY,
            't': title
        }
        response = requests.get(OMDB_API_URL, params=params)
        return response.json() if response.status_code == 200 else None
    except Exception as error:
        print(f'Error thrown invoking OMDB API', params, error, traceback.format_exc())
        return None
