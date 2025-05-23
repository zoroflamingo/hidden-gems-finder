from fastapi import FastAPI
from app.models.base import Base
from app.core.db import SessionLocal, engine
from app.routers import track, user, favorite, user_favorites, top_tracks, spotify
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(track.router)
app.include_router(user.router)
app.include_router(favorite.router)
app.include_router(user_favorites.router)
app.include_router(top_tracks.router)
app.include_router(spotify.router)


@app.get("/")
async def root():
    return {"message": "Hidden tracks Finder API is up and running!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
