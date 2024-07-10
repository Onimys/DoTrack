from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from src.core.settings import settings
from src.projects.routers import router as projects_router

app = FastAPI(
    title="dotrack.projects",
    description="Manage projects and workpaces.",
)

api_router = APIRouter()
api_router.include_router(projects_router)

app.include_router(api_router, prefix="/api")


@app.get("/health", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})


print(settings)
