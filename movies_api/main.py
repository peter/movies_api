from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Movies API")

@app.get("/health", response_class=JSONResponse)
def health():
    return { 'status': 'ok' }
