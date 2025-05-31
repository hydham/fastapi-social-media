from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import get_db, engine
from sqlalchemy.orm import Session
from . import models
from contextlib import asynccontextmanager
from .routers import post, user

SECRET_KEY = "5ff03991ebc18f8182bf0181ba352259598bc9ecb4a7ab719e14b366f6564b0e"
ALGORITH = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=post.router, prefix="/posts")
app.include_router(router=user.router, prefix="/users")


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
