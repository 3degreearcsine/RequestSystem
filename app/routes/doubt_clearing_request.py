from sqlalchemy.orm import Session
from app import schemas, oauth2, utils, exceptions
from app.dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException
from app.dbase.database import get_db, session
from pydantic.class_validators import List

router = APIRouter(tags=['Doubt Clearing Request'])


@router.post("/student_profile/dcsr/new_dcsr", status_code=status.HTTP_201_CREATED, response_model=schemas.DCSReqOut)
def user_new_dcsrf(response: Response, n_dcsreq: schemas.DCSReq, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        match_sub = utils.check_course(current_user.id, n_dcsreq.subject)
        if match_sub:
            new_dcsreq = models.SessionRequest(stu_email=current_user.email, **n_dcsreq.dict())
            db.add(new_dcsreq)
            db.commit()
            db.refresh(new_dcsreq)
            session.remove()
            return new_dcsreq
        session.remove()
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid course name")
    session.remove()
    raise exceptions.ForbiddenException


@router.get("/student_profile/dcsr/dcsr_history", response_model=List[schemas.DCSReqOut])
def user_dcsrf_history(response: Response, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        dcsrf_his = db.query(models.SessionRequest).filter(models.SessionRequest.stu_email == current_user.email).all()
        session.remove()
        return dcsrf_his
    session.remove()
    raise exceptions.ForbiddenException


@router.delete("/student_profile/dcsr/delete_dcsr")
def user_delete_dcsrf(response: Response, d_req: schemas.ReqDelete, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        result_del = db.query(models.SessionRequest).filter(models.SessionRequest.stu_email == current_user.email,
                                                            models.SessionRequest.req_id == d_req.req_id).first()
        if result_del is None:
            session.remove()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Request with id: {d_req.req_id} does not exist")
        if result_del.req_status == "pending":
            del_req.delete(synchronize_session=False)
            db.commit()
            session.remove()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    session.remove()
    raise exceptions.ForbiddenException
