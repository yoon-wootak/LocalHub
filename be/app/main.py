from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.chat import router as chat_router
from app.api.routers.health import router as health_router
from app.api.routers.import_data import router as import_router
from app.api.routers.posts import router as posts_router
from app.api.routers.locations import router as locations_router
from app.api.routers.places import router as places_router
from app.api.routers.tourism import router as tourism_router
from app.db.base import Base
from app.db.session import engine


app = FastAPI(
    title="LocalHub API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://localhub3team.netlify.app/",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(import_router)
app.include_router(posts_router)
app.include_router(locations_router)
app.include_router(places_router)
app.include_router(chat_router)
app.include_router(tourism_router)