from sqlalchemy.orm import Session
import schemas
from dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException
import oauth2
from dbase.database import get_db
from pydantic.class_validators import List

router = APIRouter(tags=['Recording Request'])

@router.post("/profile/new_rrf", status_code=status.HTTP_201_CREATED, response_model=schemas.RecReqOut)
def user_new_rrf(n_req: schemas.RecReq, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_req = models.RecRequest(stu_email=current_user.email, **n_req.dict())
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req


@router.get("/profile/rrf_history", response_model=List[schemas.RecReqOut])
def user_rrf_history(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    rrf_his = db.query(models.RecRequest).filter(models.RecRequest.stu_email == current_user.email).all()
    return rrf_his


@router.delete("/profile/delete_rrf")
def user_delete_rrf(d_req: schemas.ReqDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    del_req = db.query(models.RecRequest).filter(models.RecRequest.stu_email == current_user.email,
                                                 models.RecRequest.req_id == d_req.req_id)
    if del_req.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request with id: {d_req.req_id} does not exist")
    del_req.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/profile/action_rrf")
def admin_action_rrf(a_req: schemas.ReqAction, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    act_req = db.query(models.RecRequest).filter(models.RecRequest.req_id == a_req.req_id)
    if act_req.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request with id: {a_req.req_id} does not exist")
    act_req.update(a_req.dict(), synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
