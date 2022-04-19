from sqlalchemy.orm import Session
import schemas
import utils
from dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException
import oauth2
from dbase.database import get_db, session
from pydantic.class_validators import List

router = APIRouter(tags=['Doubt Clearing Request'])


@router.post("/student_profile/dcsr/new_dcsf", status_code=status.HTTP_201_CREATED, response_model=schemas.DCSReqOut)
def user_new_dcsrf(n_dcsreq: schemas.DCSReq, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Student':
        match_sub = utils.check_course(n_dcsreq.subject)
        if match_sub:
            new_dcsreq = models.SessionRequest(stu_email=current_user.email, **n_dcsreq.dict())
            db.add(new_dcsreq)
            db.commit()
            db.refresh(new_dcsreq)
            return new_dcsreq
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid course name")
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/student_profile/dcsr/dcsf_history", response_model=List[schemas.DCSReqOut])
def user_dcsrf_history(db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Student':
        dcsrf_his = db.query(models.SessionRequest).filter(models.SessionRequest.stu_email == current_user.email).all()
        return dcsrf_his
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.delete("/student_profile/dcsr/delete_dcsf")
def user_delete_rrf(d_req: schemas.ReqDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    del_req = db.query(models.SessionRequest).filter(models.SessionRequest.stu_email == current_user.email,
                                                     models.SessionRequest.req_id == d_req.req_id)
    result_del = del_req.first()
    if current_user.role == 'Student':
        if result_del == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Request with id: {d_req.req_id} does not exist")
        if result_del.req_status == "Pending":
            del_req.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_403_FORBIDDEN)


