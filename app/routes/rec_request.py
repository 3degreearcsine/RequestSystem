from sqlalchemy.orm import Session
from app import schemas, oauth2, utils
from app.dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException
from app.dbase.database import get_db
from pydantic.class_validators import List

router = APIRouter(tags=['Recording Request'])


@router.post("/student_profile/rr/new_rrf", status_code=status.HTTP_201_CREATED, response_model=schemas.RecReqOut)
def user_new_rrf(n_req: schemas.RecReq, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Student':
        match_req_sub = utils.check_course(current_user.id, n_req.subject)
        if match_req_sub:
            new_req = models.RecRequest(stu_email=current_user.email, **n_req.dict())
            db.add(new_req)
            db.commit()
            db.refresh(new_req)
            return new_req
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid course name")
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/student_profile/rr/rrf_history", response_model=List[schemas.RecReqOut])
def user_rrf_history(db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Student':
        rrf_his = db.query(models.RecRequest).filter(models.RecRequest.stu_email == current_user.email).all()
        return rrf_his
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.delete("/student_profile/rr/delete_rrf")
def user_delete_rrf(d_req: schemas.ReqDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    del_req = db.query(models.RecRequest).filter(models.RecRequest.stu_email == current_user.email,
                                                 models.RecRequest.req_id == d_req.req_id)
    result_del = del_req.first()
    if current_user.role == 'Student':
        if del_req.first() == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Request with id: {d_req.req_id} does not exist")
        if result_del.req_status == "Pending":
            del_req.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_403_FORBIDDEN)
