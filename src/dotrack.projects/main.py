import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from src.auth.routes import router as auth_router
from src.core.logging import init_logging
from src.core.settings import settings
from src.projects.routes import router as projects_router

init_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Application running in {'debug' if settings.DEBUG else 'production'} mode.")

    yield


app = FastAPI(
    title="dotrack.projects",
    description="Manage projects and workpaces.",
    lifespan=lifespan,
)

api_router = APIRouter()
api_router.include_router(projects_router)
api_router.include_router(auth_router)
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["v1"])


@app.get("/health", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})
