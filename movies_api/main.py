from fastapi import FastAPI
from fastapi.responses import JSONResponse
from movies_api.database import connect_with_connector

app = FastAPI(title="Movies API")

engine = connect_with_connector()
conn = engine.connect()
print(conn)

@app.get("/health", response_class=JSONResponse)
def health():
    return { 'status': 'ok' }
