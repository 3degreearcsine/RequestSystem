from fastapi import FastAPI, Depends, Response, status, HTTPException
from pydantic.class_validators import List
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

@app.get("/profile",  response_model=schemas.UserDetails)
def user_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    user = db.query(models.Users).filter(models.Users.id == current_user.id).first()

    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user

@app.post("/profile/new_rrf", status_code=status.HTTP_201_CREATED, response_model=schemas.RecReqOut)
def user_new_rrf(n_req: schemas.RecReq, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_req = models.RecRequest(stu_email=current_user.email, **n_req.dict())
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req

@app.get("/profile/rrf_history", response_model=List[schemas.RecReqOut])
def user_rrf_history(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    rrf_his = db.query(models.RecRequest).filter(models.RecRequest.stu_email == current_user.email).all()
    # print(rrf_his)
    return rrf_his

@app.post("/profile/new_dcsf", status_code=status.HTTP_201_CREATED, response_model=schemas.DCSReqOut)
def user_new_dcsrf(n_dcsreq: schemas.DCSReq, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_dcsreq = models.SessionRequest(stu_email=current_user.email, **n_dcsreq.dict())
    db.add(new_dcsreq)
    db.commit()
    db.refresh(new_dcsreq)
    return new_dcsreq

@app.get("/profile/dcsf_history", response_model=List[schemas.DCSReqOut])
def user_dcsf_history(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    dcsf_his = db.query(models.SessionRequest).filter(models.SessionRequest.stu_email == current_user.email).all()
    # print(rrf_his)
    return dcsf_his

