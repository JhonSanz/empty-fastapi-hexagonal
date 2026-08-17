from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.database_connection import engine
from src.common.exceptions_mapping import ALL_EXCEPTIONS
from src.common.router import api_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

for handler, exc_class in ALL_EXCEPTIONS:
    app.add_exception_handler(exc_class, handler)


# NOTE: allow_origins can't be "*" while allow_credentials=True (browsers reject it).
# List explicit origins here; settings.frontend_url covers the deployed frontend.
origins = [
    settings.frontend_url,
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
