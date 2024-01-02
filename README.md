# Movies API

A simple REST API example implemented with FastAPI and Postgres using [OMDB API data](https://www.omdbapi.com/)
that is deployed to GCP.

## Developer Setup

Dependencies:

* Python 3.11
* Poetry for Python package management
* Postgres

```sh
poetry install

poetry shell
# To exit shell use: deactivate

# Start server
uvicorn movies_api.main:app --host 0.0.0.0 --port 8080
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

## Resources

Libraries and frameworks:

* [FastAPI - Python web framework](https://fastapi.tiangolo.com/)
* [Poetry - Python package management](https://python-poetry.org/)
