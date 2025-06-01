from fastapi import APIRouter, Depends, status, HTTPException
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    # check email already exists
    email_exist = db.query(models.User).filter_by(email=user.email).first()
    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email exists"
        )

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=id).first()
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No user exists"
        )

    return user
