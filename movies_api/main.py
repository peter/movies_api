from fastapi import FastAPI
from movies_api.database import db_connect
from movies_api.routes import api_docs, health, movies

app = FastAPI(title="Movies API")

db_connect()

app.include_router(api_docs.router)
app.include_router(health.router)
app.include_router(movies.router)
