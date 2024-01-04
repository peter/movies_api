import os
import pytest
from fastapi.testclient import TestClient

from movies_api.main import app

client = TestClient(app)

def test_movies_list():
    movies = [
        {'title': 'The Shining'},
        {'title': 'The Hours'},
        {'title': 'Juno'},
    ]
    for movie in movies:
        response = client.post("/movies", json=movie)
        assert response.status_code == 200    

    response = client.get("/movies")
    assert response.status_code == 200
    assert response.json() == {
        'data': [
            {'id': 3, 'title': 'Juno'},
            {'id': 2, 'title': 'The Hours'},
            {'id': 1, 'title': 'The Shining'},
        ]
    }    

    response = client.get("/movies?limit=1")
    assert response.status_code == 200
    assert response.json() == {
        'data': [
            {'id': 3, 'title': 'Juno'},
        ]
    }    

    response = client.get("/movies?limit=1&offset=1")
    assert response.status_code == 200
    assert response.json() == {
        'data': [
            {'id': 2, 'title': 'The Hours'},
        ]
    }    

def test_movies_get():
    movie = {'title': 'Barbie'}
    response = client.post("/movies", json=movie)
    assert response.status_code == 200    
    created_movie = response.json()

    response = client.get(f'/movies/{created_movie["id"]}')
    assert response.status_code == 200    
    assert response.json() == {
        'id': created_movie['id'],
        **movie
    }

    response = client.get(f'/movies/1234567')
    assert response.status_code == 404

    response = client.get(f'/movies/foobar')
    assert response.status_code == 422

def test_movies_omdb_add():
    if not os.environ.get('OMDB_API_KEY'):
        pytest.skip('Cannot test movies_omdb_add endpoint without OMDB_API_KEY')

    movie = {'title': 'The Celebration'} # i.e. "Festen"
    response = client.post("/movies/omdb-add", json=movie)
    assert response.status_code == 200    
    created_movie = response.json()
    assert created_movie['title'] == movie['title']
    assert created_movie['year'] == 1998
    assert created_movie['genre'] == 'Drama'
    assert created_movie['director'] == 'Thomas Vinterberg'
    assert created_movie['writer'].find('Thomas Vinterberg') != -1
    assert created_movie['runtime'] == 105
    assert type(created_movie['imdb_rating']) == float
    assert created_movie['imdb_rating'] > 7.0
    assert created_movie['actors'].find('Thomas Bo Larsen') != -1
    assert created_movie['plot'].find('birthday') != -1
    assert created_movie['language'].find('Danish') != -1

    response = client.get(f'/movies/{created_movie["id"]}')
    assert response.status_code == 200
    assert response.json() == created_movie

def test_movies_create():
    movie = {
        'title': 'Oppenheimer',

        'plot': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.',
        'language': 'English, German, Italian',
        'country': 'United States, United Kingdom',
        'director': 'Christopher Nolan',

        'year': 2023,
        'runtime': 180,
        'imdb_rating': 8.4,

        'writer': 'Christopher Nolan, Kai Bird, Martin Sherwin',
        'genre': 'Biography, Drama, History',
        'actors': 'Cillian Murphy, Emily Blunt, Matt Damon',
    }
    response = client.post('/movies', json=movie)
    assert response.status_code == 200    
    created_movie = response.json()

    response = client.get(f'/movies/{created_movie["id"]}')
    assert response.status_code == 200    
    assert response.json() == {
        'id': created_movie['id'],
        **movie
    }

    # Invalid field type
    invalid_movie = { **movie, 'year': 'foobar'}
    response = client.post("/movies", json=invalid_movie)
    assert response.status_code == 422

    # Title is required
    invalid_movie = { **movie, 'title': None}
    response = client.post("/movies", json=invalid_movie)
    assert response.status_code == 422

def test_movies_update():
    movie = {'title': 'Barbie'}
    response = client.post("/movies", json=movie)
    assert response.status_code == 200    
    created_movie = response.json()

    # Successful update
    updated_movie={**created_movie, 'title': 'foobar', 'year': 2023}
    response = client.put(f'/movies/{created_movie["id"]}', json=updated_movie)
    assert response.status_code == 200
    assert response.json()['title'] == updated_movie['title']

    response = client.get(f'/movies/{created_movie["id"]}')
    assert response.status_code == 200    
    assert response.json() == updated_movie

    # Invalid field type
    invalid_movie={**created_movie, 'title': 123}
    response = client.put(f'/movies/{created_movie["id"]}', json=invalid_movie)
    assert response.status_code == 422

    # Movie is unchanged
    response = client.get(f'/movies/{created_movie["id"]}')
    assert response.status_code == 200    
    assert response.json() == updated_movie

    # Missing ID
    response = client.put(f'/movies/1234567', json=updated_movie)
    assert response.status_code == 404

def test_movies_delete():
    movie = {'title': 'Barbie'}
    response = client.post("/movies", json=movie)
    assert response.status_code == 200    
    created_movie = response.json()

    response = client.delete(f'/movies/{created_movie["id"]}')
    assert response.status_code == 204

    response = client.get(f'/movies/{created_movie["id"]}')
    assert response.status_code == 404

    response = client.delete(f'/movies/{created_movie["id"]}')
    assert response.status_code == 404
