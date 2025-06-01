from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import get_db, engine
from sqlalchemy.orm import Session
from . import models
from contextlib import asynccontextmanager
from .routers import post, user, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Social Media API",
    description="Fastapi APIS for social media application",
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="postgres",
        port=5432,
        cursor_factory=RealDictCursor,
    )

    cursor = conn.cursor()
    print("Database connected")
except Exception as error:
    print("Database connection failed")
    print("Error: ", error)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
async def test_db(db: Session = Depends(get_db)):
    db.query("")
    return {"message": "success"}
