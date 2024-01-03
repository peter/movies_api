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
