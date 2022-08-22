from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import schemas, oauth2, exceptions
from app.dbase import models, database
from fastapi import Depends, status, APIRouter, Response, HTTPException
from app.dbase.database import get_db
from pydantic.class_validators import List

router = APIRouter(tags=['Administration'])


@router.get("/admin_profile/all_students", response_model=List[schemas.AllStudents])
def all_students(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        stu_profiles = db.query(models.Users, models.Student).join(models.Student, models.Student.user_id ==
                                                                   models.Users.id, isouter=False).all()
        database.session.remove()
        return stu_profiles
    database.session.remove()
    raise exceptions.ForbiddenException


@router.get("/admin_profile/all_tutors", response_model=List[schemas.AllTutors])
def all_tutors(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        tut_profiles = db.query(models.Users, models.Tutor).join(models.Tutor, models.Tutor.user_id == models.Users.id,
                                                                 isouter=False).all()
        database.session.remove()
        return tut_profiles
    database.session.remove()
    raise exceptions.ForbiddenException


@router.get("/admin_profile/requests/all_pending_rr")
def all_pending_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        rrf_act_pending = db.query(models.RecRequest).filter(models.RecRequest.req_status == 'pending').all()
        database.session.remove()
        return rrf_act_pending
    database.session.remove()
    raise exceptions.ForbiddenException


@router.get("/admin_profile/requests/all_pending_dcsr")
def all_pending_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        dcsf_act_pending = db.query(models.SessionRequest).filter(or_(models.SessionRequest.req_status == 'pending',
                                                                      models.SessionRequest.req_status == 'forwarded')
                                                                  ).all()
        database.session.remove()
        return dcsf_act_pending
    database.session.remove()
    raise exceptions.ForbiddenException


@router.put("/admin_profile/requests/all_pending_rr/action_rr")
def admin_action_rrf(a_req: schemas.ReqAction, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        act_req = db.query(models.RecRequest).filter(models.RecRequest.req_id == a_req.req_id)
        if act_req.first() is None:
            database.session.remove()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Recording request with id: {a_req.req_id} does not exist")
        act_req.update(a_req.dict(), synchronize_session=False)
        db.commit()
        database.session.remove()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    database.session.remove()
    raise exceptions.ForbiddenException


@router.put("/admin_profile/requests/all_pending_dcsr/action_dcsr")
def admin_action_dcsf(a_req: schemas.ReqAction, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        act_req = db.query(models.SessionRequest).filter(models.SessionRequest.req_id == a_req.req_id)
        if act_req.first() is None:
            database.session.remove()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Doubt clearing session request with id: {a_req.req_id} does not exist")
        act_req.update(a_req.dict(), synchronize_session=False)
        db.commit()
        database.session.remove()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    database.session.remove()
    raise exceptions.ForbiddenException




