from sqlalchemy.orm import Session
from app import schemas, oauth2, utils
from app.dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException
from app.dbase.database import get_db, session
from pydantic.class_validators import List

router = APIRouter(tags=['User Profile'])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.Registration, db: Session = Depends(get_db)):
    if user.role == 'Admin':
        admin_exist = utils.check_if_admin_exist(user.role)
        print(admin_exist)
        if admin_exist:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        new_user = models.Users(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        session.remove()
        return {
            "data": "Registration Successful."
        }

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    session.remove()
    return {
        "data": "Registration Successful."
    }

@router.post("/complete_student_profile")
def add_student_info(student: schemas.StudentInfo, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Student':
        new_student = models.Student(user_id=current_user.id, **student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return Response(status_code=status.HTTP_201_CREATED)
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/student_profile", response_model=schemas.StudentAllDetails)
def student_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Left outer join
    s_updated_profile = db.query(models.Users, models.Student).join(models.Student, models.Student.user_id == models.Users.id,
                                                                    isouter=True).filter(
        models.Student.user_id == current_user.id).first()
    return s_updated_profile


@router.post("/complete_admin_profile")
def add_admin_info(admin: schemas.AdminInfo, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Admin':
        new_admin = models.Admin(user_id=current_user.id, **admin.dict())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return Response(status_code=status.HTTP_201_CREATED)
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/admin_profile", response_model=schemas.AdminAllDetails)
def admin_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Left outer join
    a_updated_profile = db.query(models.Users, models.Admin).join(models.Admin, models.Admin.user_id == models.Users.id,
                                                                  isouter=True).filter(
        models.Admin.user_id == current_user.id).first()
    return a_updated_profile


@router.post("/complete_tutor_profile")
def add_tutor_info(tutor: schemas.TutorInfo, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'Tutor':
        new_tutor = models.Tutor(user_id=current_user.id, **tutor.dict())
        db.add(new_tutor)
        db.commit()
        db.refresh(new_tutor)
        return Response(status_code=status.HTTP_201_CREATED)
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/tutor_profile", response_model=schemas.TutorAllDetails)
def tutor_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Left outer join
    t_updated_profile = db.query(models.Users, models.Tutor).join(models.Tutor, models.Tutor.user_id == models.Users.id,
                                                                  isouter=True).filter(
        models.Tutor.user_id == current_user.id).first()
    return t_updated_profile

