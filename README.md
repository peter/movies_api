# Movies API

A simple REST API example implemented with FastAPI and Postgres using [OMDB API data](https://www.omdbapi.com/) that is deployed to GCP.

## Developer Setup

Dependencies:

* Python 3.11
* Poetry for Python package management
* Postgres

```sh
poetry install

poetry shell
# To exit shell use: deactivate

# Create database
createdb -U postgres movies_api

# Start development server (starts uvicorn on port 8080)
bin/start-dev

open http://localhost:8080
```

## Testing

Pytest is used for testing and the tests are in [test_movies.py](movies_api/routes/test_movies.py)

```sh
# Run the pytest tests (this will recreate the movies_api_test database first)
bin/test

# In order to test the endpoint that adds movie from OMDB you need the OMDB API key:
OMDB_API_KEY=... bin/test
```

## Invoking the API with Curl

```sh
export LOCAL_BASE_URL=http://localhost:8080
export PRODUCTION_BASE_URL=https://movies-api-6yotxag7iq-ew.a.run.app
export BASE_URL=$LOCAL_BASE_URL

#######################################
# list endpoint
#######################################

# List movies (default limit is 10, sorting is by title ascending)
curl -s $BASE_URL/movies | jq
# List second page of movies
curl -s $BASE_URL/movies?offset=10 | jq
# List all movies
curl -s $BASE_URL/movies?limit=300 | jq
# Find movie(s) by title (title does not have a unique constraint)
curl -s $BASE_URL/movies?title=Whiplash | jq

#######################################
# get endpoint
#######################################

# Get movie by id
curl -s $BASE_URL/movies/1 | jq
# Unknown id yields 404 Not Found
curl -i $BASE_URL/movies/123456
# Invalid id yields 422 Unprocessable Entity
curl -i $BASE_URL/movies/asdf

#######################################
# add movie from OMDB endpoint
#######################################

# Successful add - returns created movie with ID
curl -H "Content-Type: application/json" -X POST -d '{"title":"The Hours"}' $BASE_URL/movies/omdb-add | jq
# Invalid add yields 422 Unprocessable Entity with a validation error message from Pydantic
curl -i -H "Content-Type: application/json" -X POST -d '{"titless":"The Hours"}' $BASE_URL/movies/omdb-add
# If the movie title doesn't exist in OMDB we get a 404
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"foooooobar"}' $BASE_URL/movies/omdb-add

#######################################
# create endpoint
#######################################

# Successful create - returns created movie with ID
curl -H "Content-Type: application/json" -X POST -d '{"title":"The Hours"}' $BASE_URL/movies | jq
# Invalid create yields 422 Unprocessable Entity with a validation error message from Pydantic
curl -i -H "Content-Type: application/json" -X POST -d '{"title":123}' $BASE_URL/movies

#######################################
# update endpoint
#######################################

# Successful update
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Awesome Movie"}' $BASE_URL/movies/1
# An invalid request body yields a 422 Unprocessable Entity with a validation error message from Pydantic
curl -i -H "Content-Type: application/json" -X PUT -d '{"titles":"Awesome Movie"}' $BASE_URL/movies/1
# A non-existant ID yields a 404
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Awesome Movie"}' $BASE_URL/movies/12345

#######################################
# delete endpoint
#######################################

# Successful delete yields 204 No Content
curl -i -X DELETE -u 'joe:secret' $BASE_URL/movies/1
# A non-existant ID yields a 404
curl -i -X DELETE -u 'joe:secret' $BASE_URL/movies/12345
```

## Running Script to Import OMDB Movies

To populate local Postgres database:

```sh
OMDB_API_KEY=... DB_HOST=localhost DB_PASS=postgres poetry run python bin/omdb-import
```

To populate Cloud SQL database:

```sh
OMDB_API_KEY=... INSTANCE_CONNECTION_NAME=moviesapi-409007:europe-west1:movies-api DB_PASS=... poetry run python bin/omdb-import
```

## Deployment

The API is deployed as a Docker image on GCP with Cloud Run at [movies-api-6yotxag7iq-ew.a.run.app](https://movies-api-6yotxag7iq-ew.a.run.app/docs). There is a [deploy script](bin/deploy) that builds and pushes a new Docker image based on the local source code and deploys it to Cloud Run. The Cloud run service has continuous deployment option that would make commits to master be automatically deployed to Cloud Run.

## API Docs

```sh
# OpenAPI Docs (also available at the root):
open http://localhost:8080/docs

# The OpenAPI/Swagger spec:
open http://localhost:8080/openapi.json
```

## Dislaimer/Scope/Discussion

* The [SQLModel library](https://github.com/tiangolo/sqlmodel) (a compatible wrapper on top of SQLLachemy and Pydantic) could offer a way to avoid duplicating the model schema
* Database data should be cleared out between each test to avoid risk of test interference
* The delete endpoint would be more efficient if it didn't fetch the record before deleting it
* Linting, more type hints, and potentially code formating should be added

## Resources

Libraries and frameworks:

* [FastAPI and SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
* [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
* [SQLModel package - combines Pydandic with SQLAlchemy](https://github.com/tiangolo/sqlmodel)
* [Python ORM Alternatives](https://www.infoworld.com/article/3709854/6-orms-for-every-database-powered-python-app.html)
* [Poetry - Python package management](https://python-poetry.org/)
