# Movies API

A simple REST API example implemented with FastAPI and Postgres using [OMDB API data](https://www.omdbapi.com/)

## Developer Setup

```sh
poetry install

poetry shell
# deactivate

# Start server
uvicorn movies_api.main:app --host 0.0.0.0 --port 8080
```

## API Docs

```sh
# OpenAPI Docs are available under /docs
open http://localhost:8080/docs
```

## Invoke API with Curl

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
