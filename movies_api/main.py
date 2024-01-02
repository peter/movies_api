from fastapi import FastAPI
from fastapi.responses import JSONResponse
from movies_api.database import db_engine

app = FastAPI(title="Movies API")

engine = db_engine()
conn = engine.connect()

@app.get("/health", response_class=JSONResponse)
def health():
    return { 'status': 'ok' }
