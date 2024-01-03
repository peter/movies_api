from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

# Root redirects to OpenAPI documentation
@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')
