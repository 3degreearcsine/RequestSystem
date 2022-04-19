from sqlalchemy.orm import Session
from sqlalchemy import or_
import schemas
from dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException
import oauth2
from dbase.database import get_db
from pydantic.class_validators import List

router = APIRouter(tags=['Administration'])

@router.get("/admin_profile/all_students", response_model=List[schemas.AllStudents])
# @router.get("/admin_profile/all_students")
def all_students(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Admin':
        stu_profiles = db.query(models.Users, models.Student).join(models.Student, models.Student.user_id == models.Users.id,
                                                                   isouter=False).all()
        return stu_profiles
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/admin_profile/all_tutors", response_model=List[schemas.AllTutors])
def all_tutors(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Admin':
        tut_profiles = db.query(models.Users, models.Tutor).join(models.Tutor, models.Tutor.user_id == models.Users.id,
                                                                 isouter=False).all()
        return tut_profiles
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/admin_profile/requests/all_pending_rrf")
def all_pending_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Admin':
        rrf_act_pending = db.query(models.SessionRequest).filter(models.SessionRequest.req_status == 'Pending').all()
        return rrf_act_pending
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/admin_profile/requests/all_pending_dcsf")
def all_pending_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Admin':
        dcsf_act_pending = db.query(models.SessionRequest).filter(or_(models.SessionRequest.req_status == 'Pending',
                                                                      models.SessionRequest.req_status == 'Forwarded')).all()
        return dcsf_act_pending
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.put("/admin_profile/requests/all_pending_rrf/action_rrf")
def admin_action_rrf(a_req: schemas.ReqAction, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Admin':
        act_req = db.query(models.RecRequest).filter(models.RecRequest.req_id == a_req.req_id)
        if act_req.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Recording request with id: {a_req.req_id} does not exist")
        act_req.update(a_req.dict(), synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.put("/admin_profile/requests/all_pending_dcsf/action_dcsf")
def admin_action_dcsf(a_req: schemas.ReqAction, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Admin':
        act_req = db.query(models.SessionRequest).filter(models.SessionRequest.req_id == a_req.req_id)
        if act_req.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Doubt clearing session request with id: {a_req.req_id} does not exist")
        act_req.update(a_req.dict(), synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_403_FORBIDDEN)




