from sqlalchemy.orm import Session
from app import schemas, oauth2, utils, exceptions
from app.dbase import models, database
from fastapi import Depends, status, APIRouter, Response, HTTPException
from app.dbase.database import get_db
from pydantic.class_validators import List

router = APIRouter(tags=['Recording Request'])


@router.post("/student_profile/rr/new_rr", status_code=status.HTTP_201_CREATED, response_model=schemas.RecReqOut)
def user_new_rrf(n_req: schemas.RecReq, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        match_req_sub = utils.check_course(current_user.id, n_req.subject)
        if match_req_sub:
            new_req = models.RecRequest(stu_email=current_user.email, **n_req.dict())
            db.add(new_req)
            db.commit()
            db.refresh(new_req)
            database.session.remove()
            return new_req
        database.session.remove()
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid course name")
    database.session.remove()
    raise exceptions.ForbiddenException


@router.get("/student_profile/rr/rr_history", response_model=List[schemas.RecReqOut])
def user_rrf_history(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        rrf_his = db.query(models.RecRequest).filter(models.RecRequest.stu_email == current_user.email).all()
        database.session.remove()
        return rrf_his
    database.session.remove()
    raise exceptions.ForbiddenException


@router.delete("/student_profile/rr/delete_rr")
def user_delete_rrf(d_req: schemas.ReqDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        del_req = db.query(models.RecRequest).filter(models.RecRequest.stu_email == current_user.email,
                                                     models.RecRequest.req_id == d_req.req_id)
        result_del = del_req.first()
        if result_del is None:
            database.session.remove()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Request with id: {d_req.req_id} does not exist")
        if result_del.req_status == "pending":
            del_req.delete(synchronize_session=False)
            db.commit()
            database.session.remove()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    database.session.remove()
    raise exceptions.ForbiddenException
