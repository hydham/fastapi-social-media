from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .. import models, utils, oauth2, schemas
from sqlalchemy.orm import Session
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(
    user_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password"
    )

    # get the user by email
    user = db.query(models.User).filter_by(email=user_form.username).first()
    if not user:
        raise credentials_exception

    # verify password
    if not utils.verify_password(user_form.password, user.password):
        raise credentials_exception

    # create a token
    # return a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
