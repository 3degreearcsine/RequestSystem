from sqlalchemy.orm import Session
from app import schemas, oauth2, utils, exceptions
from app.dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException
from app.dbase.database import get_db
from pydantic.class_validators import List

router = APIRouter(tags=['Staff'])

@router.get("/tutur_profile/requests_dcsf")
def all_pending_requests(response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'tutor':
        chk_tut_sub = utils.check_tutor_course(current_user.id)

        dcsf_a_pending = db.query(models.SessionRequest).filter(models.SessionRequest.subject == chk_tut_sub.tutor_of).filter(
            models.SessionRequest.req_status == 'Forwarded').all()
        return dcsf_a_pending
    raise exceptions.ForbiddenException


@router.put("/tutor_profile/requests_dcsf/action_dcsf")
def tutor_action_dcsf(response: Response, t_req: schemas.ReqAction, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'tutor':
        act_req = db.query(models.SessionRequest).filter(models.SessionRequest.req_id == t_req.req_id)
        if act_req.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Request with id: {t_req.req_id} does not exist")
        if t_req.req_status in ('Accepted', 'Rejected'):
            act_req.update(t_req.dict(), synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=f"Invalid Input {t_req.req_status}")
    raise exceptions.ForbiddenException
