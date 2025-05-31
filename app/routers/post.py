from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts_query = db.query(models.Post).order_by(models.Post.id)
    posts = posts_query.all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # SQL = "INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *"
    # data = (new_post.title, new_post.content, new_post.published)
    # cursor.execute(SQL, data)
    # new_data = cursor.fetchone()

    # conn.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts where id = %s """, (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter_by(id=id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post with this id not found"
        )

    return post


@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter_by(id=id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found with that ID"
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(
    id: int, update_data: schemas.PostUpdate, db: Session = Depends(get_db)
):
    # cursor.execute(
    #     """ UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #     (update_data.title, update_data.content, update_data.published, id),
    # )

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter_by(id=id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(update_data.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(post)

    return post
