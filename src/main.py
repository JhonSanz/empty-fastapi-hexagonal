from fastapi import FastAPI
from src.common.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from src.common.exceptions_mapping import ALL_EXCEPTIONS


app = FastAPI()
app.include_router(api_router)

for item in ALL_EXCEPTIONS:
    app.add_exception_handler(item[1], item[0])


origins = [
    "*",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
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
