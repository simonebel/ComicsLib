from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.comics import router as comics_router
from api.home import router as home_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "Connection",
        "Accept-Ranges",
    ],
)

app.include_router(comics_router.router)
app.include_router(home_router.router)
