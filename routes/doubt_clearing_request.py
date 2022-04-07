from sqlalchemy.orm import Session
import schemas
from dbase import models
from fastapi import Depends, status, APIRouter
import oauth2
from dbase.database import get_db
from pydantic.class_validators import List
router = APIRouter(tags=['Doubt Clearing Request'])

@router.post("/profile/new_dcsf", status_code=status.HTTP_201_CREATED, response_model=schemas.DCSReqOut)
def user_new_dcsrf(n_dcsreq: schemas.DCSReq, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_dcsreq = models.SessionRequest(stu_email=current_user.email, **n_dcsreq.dict())
    db.add(new_dcsreq)
    db.commit()
    db.refresh(new_dcsreq)
    return new_dcsreq


@router.get("/profile/dcsf_history", response_model=List[schemas.DCSReqOut])
def user_dcsrf_history(db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    dcsrf_his = db.query(models.SessionRequest).filter(models.SessionRequest.stu_email == current_user.email).all()
    return dcsrf_his