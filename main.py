from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import utils
import auth
import oauth2
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)

@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.RegiOut)
def create_user(user: schemas.Registration, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/profile/{id}",  response_model=schemas.UserDetails)
def user_profile(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user



