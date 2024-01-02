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
```

## Running Script to Import OMDB Movies

To populate local Postgres database:

```sh
PYTHONPATH=. DB_HOST=localhost DB_PASS=postgres poetry run python bin/import-omdb-movies
```

To populate Cloud SQL database:

```sh
PYTHONPATH=. INSTANCE_CONNECTION_NAME=moviesapi-409007:europe-west1:movies-api DB_PASS=... poetry run python bin/import-omdb-movies
```

## Deployment

The API is deployed as a Docker image on GCP with Cloud Run at [movies-api-6yotxag7iq-ew.a.run.app](https://movies-api-6yotxag7iq-ew.a.run.app/docs). There is a [deploy script](bin/deploy) that builds and pushes a new
Docker image based on the local source code and deploys it to Cloud Run. The Cloud run service has continuous
deployment so that new commits to master are automatically deployed to Cloud Run.

## API Docs

```sh
# OpenAPI Docs are available under /docs
open http://localhost:8080/docs
```

## Invoking the API with Curl

```sh
# Health endpoint returns status 200 and JSON
curl -i http://0.0.0.0:8080/health  
curl -s http://0.0.0.0:8080/health | jq

# Unknown endpoint yields 404
curl -i http://0.0.0.0:8080
```

## Downloading OMDB Data with curl

```sh
export OMDB_API_URL=http://www.omdbapi.com
export OMDB_API_KEY=...

IFS=$'\n'
for movie_name in $(cat data/imdb-top-250-movie-titles.txt)
do
    echo $movie_name
    curl -s -G "$OMDB_API_URL/?apikey=$OMDB_API_KEY" --data-urlencode "t=$movie_name" | jq
done
```

## Resources

Libraries and frameworks:

* [FastAPI - Python web framework](https://fastapi.tiangolo.com/)
* [FastAPI and SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
* [SQLModel package - combines Pydandic with SQLAlchemy](https://github.com/tiangolo/sqlmodel)
* [Poetry - Python package management](https://python-poetry.org/)
