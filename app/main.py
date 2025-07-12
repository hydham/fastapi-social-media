from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import auth, post, user, vote


@asynccontextmanager
async def lifespan(app: FastAPI):
    # models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Social Media API",
    description="Fastapi APIS for social media application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def health_check():
    return {"message": "hello world!!!"}   
