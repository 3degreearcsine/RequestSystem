from sqlalchemy.orm import Session
import schemas
from dbase import models
import utils
from fastapi import Depends, status, APIRouter
import oauth2
from dbase.database import get_db

router = APIRouter(tags=['User Profile'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.RegistrationOut)
def create_user(user: schemas.Registration, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/profile",  response_model=schemas.UserDetails)
def user_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == current_user.id).first()
    return user

