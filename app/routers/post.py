from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import func
from .. import models, schemas
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=list[schemas.PostOut])
# @router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(get_current_user),
    limit: int = 10,
    skip: Optional[int] = None,
    search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts_query = (
        db.query(models.Post)
        .options(joinedload(models.Post.owner))
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    )

    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id).all()
    )
    print(result)

    posts = posts_query.all()

    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(get_current_user),
):
    # SQL = "INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *"
    # data = (new_post.title, new_post.content, new_post.published)
    # cursor.execute(SQL, data)
    # new_data = cursor.fetchone()

    # conn.commit()

    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(get_current_user),
):
    # cursor.execute(""" SELECT * FROM posts where id = %s """, (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter_by(id=id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post with this id not found"
        )

    return post


@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(get_current_user),
):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter_by(id=id, owner_id=current_user.id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or unauthoized delete",
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(
    id: int,
    update_data: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(get_current_user),
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid post id"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update"
        )

    post_query.update(update_data.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(post)

    return post
