from sqlalchemy.orm import Session
from app import schemas, oauth2, utils
from app.dbase import models
from fastapi import Depends, status, APIRouter, Response, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dbase.database import get_db, session
from app import main


router = APIRouter(tags=['User Profile'])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def create_user(request: Request, user: schemas.Registration = Depends(), db: Session = Depends(get_db)):
    email_exists = utils.check_if_email_exists(user.email)
    if email_exists:
        invalid_user_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                               detail="Your email address is already registered with us.")
        return main.templates.TemplateResponse('registration.html',
                                               context={'request': request, 'error': invalid_user_exception.detail},
                                               status_code=invalid_user_exception.status_code)

    if user.role == 'admin':
        admin_exist = utils.check_if_admin_exist(user.role)
        if admin_exist:
            invalid_user_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                                   detail="Admin user already exists")
            return main.templates.TemplateResponse('registration.html',
                                                   context={'request': request,
                                                            'error': invalid_user_exception.detail},
                                                   status_code=invalid_user_exception.status_code)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    session.remove()
    data = "Registration Successful."
    return main.templates.TemplateResponse('registration.html', context={'request': request, 'data': data})


@router.get("/fill_profile_info", response_class=HTMLResponse)
def fill_profile_info(request: Request, current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        return main.templates.TemplateResponse('profile_info.html', context={'request': request, 'admin': 'admin'},
                                               status_code=status.HTTP_200_OK)
    if current_user.role == 'student':
        return main.templates.TemplateResponse('profile_info.html', context={'request': request, 'student': 'student'},
                                               status_code=status.HTTP_200_OK)
    if current_user.role == 'tutor':
        return main.templates.TemplateResponse('profile_info.html', context={'request': request, 'tutor': 'tutor'},
                                               status_code=status.HTTP_200_OK)


@router.post("/complete_student_profile", status_code=status.HTTP_201_CREATED)
def add_student_info(request: Request, response: Response, student: schemas.StudentInfo = Depends(), db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        new_student = models.Student(user_id=current_user.id, **student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        session.remove()
        stu_update_detail = "Profile Information Added"
        return main.templates.TemplateResponse('popup.html', context={'request': request,
                                                                      'stu_update_detail': stu_update_detail },
                                               status_code=status.HTTP_201_CREATED)
    error = "Access Forbidden"
    response.status_code = status.HTTP_403_FORBIDDEN
    return error


@router.get("/student_profile", response_model=schemas.StudentAllDetails)
def student_profile(response: Response, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    if current_user.role == 'student':
        if not utils.check_if_profile_complete(current_user.id, current_user.role):
            return RedirectResponse("http://127.0.0.1:8000/fill_profile_info")
        # Left outer join
        s_updated_profile = db.query(models.Users, models.Student).join(models.Student,
                                                                        models.Student.user_id == models.Users.id,
                                                                        isouter=True).filter(models.Student.user_id == current_user.id).first()
        return s_updated_profile
    error = "Access Forbidden"
    response.status_code = status.HTTP_403_FORBIDDEN
    return error


@router.post("/complete_admin_profile")
def add_admin_info(request: Request, response: Response, admin: schemas.AdminInfo = Depends(), db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        new_admin = models.Admin(user_id=current_user.id, **admin.dict())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        session.remove()
        adm_update_detail = "Profile Information Added"
        return main.templates.TemplateResponse('popup.html', context={'request': request,
                                                                      'adm_update_detail': adm_update_detail},
                                               status_code=status.HTTP_201_CREATED)
    error = "Access Forbidden"
    response.status_code = status.HTTP_403_FORBIDDEN
    return error


@router.get("/admin_profile", response_model=schemas.AdminAllDetails)
def admin_profile(response: Response, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        if not utils.check_if_profile_complete(current_user.id, current_user.role):
            return RedirectResponse("http://127.0.0.1:8000/fill_profile_info")
        # Left outer join
        a_updated_profile = db.query(models.Users, models.Admin).join(models.Admin, models.Admin.user_id == models.Users.id,
                                                                      isouter=True).filter(models.Admin.user_id == current_user.id).first()
        return a_updated_profile
    error = "Access Forbidden"
    response.status_code = status.HTTP_403_FORBIDDEN
    return error


@router.post("/complete_tutor_profile")
def add_tutor_info(request: Request, response: Response, tutor: schemas.TutorInfo = Depends(), db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'tutor':
        new_tutor = models.Tutor(user_id=current_user.id, **tutor.dict())
        db.add(new_tutor)
        db.commit()
        db.refresh(new_tutor)
        session.remove()
        tut_update_detail = "Profile Information Added"
        return main.templates.TemplateResponse('popup.html', context={'request': request,
                                                                      'tut_update_detail': tut_update_detail},
                                               status_code=status.HTTP_201_CREATED)
    error = "Access Forbidden"
    response.status_code = status.HTTP_403_FORBIDDEN
    return error


@router.get("/tutor_profile", response_model=schemas.TutorAllDetails)
def tutor_profile(response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'tutor':
        if not utils.check_if_profile_complete(current_user.id, current_user.role):
            return RedirectResponse("http://127.0.0.1:8000/fill_profile_info")
        # Left outer join
        t_updated_profile = db.query(models.Users, models.Tutor).join(models.Tutor, models.Tutor.user_id == models.Users.id,
                                                                      isouter=True).filter(models.Tutor.user_id == current_user.id).first()
        return t_updated_profile
    error = "Access Forbidden"
    response.status_code = status.HTTP_403_FORBIDDEN
    return error

