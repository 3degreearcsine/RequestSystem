from sqlalchemy.orm import Session
from app import schemas, oauth2, utils
from app.dbase import models, config
from fastapi import Depends, status, APIRouter, Response, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dbase.database import get_db, session
from app import main
from fastapi.encoders import jsonable_encoder


router = APIRouter(tags=['User Profile'])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def create_user(request: Request, user: schemas.Registration = Depends(), db: Session = Depends(get_db)):
    email_exists = utils.check_if_email_exists(user.email)
    if email_exists:
        session.remove()
        invalid_user_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                               detail="Your email address is already registered with us.")
        return main.templates.TemplateResponse('registration.html',
                                               context={'request': request, 'error': invalid_user_exception.detail,
                                                        'url': config.settings.url},
                                               status_code=invalid_user_exception.status_code)

    if user.role == 'admin':
        admin_exist = utils.check_if_admin_exist(user.role)
        if admin_exist:
            session.remove()
            invalid_user_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                                   detail="Admin user already exists")
            return main.templates.TemplateResponse('registration.html',
                                                   context={'request': request,
                                                            'error': invalid_user_exception.detail,
                                                            'url': config.settings.url},
                                                   status_code=invalid_user_exception.status_code)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    session.remove()
    data = "Registration Successful."
    return main.templates.TemplateResponse('registration.html', context={'request': request, 'data': data,
                                                                         'url': config.settings.url})


@router.get("/fill_profile_info", response_class=HTMLResponse)
def fill_profile_info(request: Request, current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        session.remove()
        return main.templates.TemplateResponse('profile_info.html', context={'request': request, 'admin': 'admin',
                                                                             'url': config.settings.url},
                                               status_code=status.HTTP_200_OK)
    if current_user.role == 'student':
        session.remove()
        return main.templates.TemplateResponse('profile_info.html', context={'request': request, 'student': 'student',
                                                                             'url': config.settings.url},
                                               status_code=status.HTTP_200_OK)
    if current_user.role == 'tutor':
        session.remove()
        return main.templates.TemplateResponse('profile_info.html', context={'request': request, 'tutor': 'tutor',
                                                                             'url': config.settings.url},
                                               status_code=status.HTTP_200_OK)


@router.post("/complete_student_profile", response_class=HTMLResponse)
def add_student_info(request: Request, response: Response, student: schemas.StudentInfo = Depends(), db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        if len(str(student.contact_no)) < 10 or len(str(student.contact_no)) > 10:
            session.remove()
            return main.templates.TemplateResponse('popup.html',
                                                   context={'request': request,
                                                            'server_error': "Contact Number must be 10 digit",
                                                            'url': config.settings.url},
                                                   status_code=status.HTTP_400_BAD_REQUEST)
        new_student = models.Student(user_id=current_user.id, **student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        session.remove()
        stu_update_detail = "Profile Information Added"
        return main.templates.TemplateResponse('popup.html', context={'request': request,
                                                                      'stu_update_detail': stu_update_detail,
                                                                      'url': config.settings.url},
                                               status_code=status.HTTP_201_CREATED)
    session.remove()
    raise exceptions.ForbiddenException


@router.get("/student_profile", response_class=HTMLResponse)
def student_profile(request: Request, response: Response, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'student':
        if not utils.check_if_profile_complete(current_user.id, current_user.role):
            return RedirectResponse(url="/fill_profile_info", status_code=status.HTTP_302_FOUND)
        # Left outer join
        s_updated_profile = db.query(models.Users, models.Student).join(models.Student,
                                                                        models.Student.user_id == models.Users.id,
                                                                        isouter=True).filter(models.Student.user_id == current_user.id).first()
        first_name = utils.check_if_email_exists(current_user.email).firstname
        last_name = utils.check_if_email_exists(current_user.email).lastname

        s_profile = schemas.StudentAllDetails.from_orm(s_updated_profile)
        json_s_profile = jsonable_encoder(s_profile)
        s_headings = ["First Name", "Last Name", "Email", "Student ID", "User ID", "Date of Birth", "Course Name",
                      "Address", "Contact No"]
        values = []
        for k, val in json_s_profile.items():
            for k2, val2 in val.items():
                values.append(val2)
        s_info_dict = dict(zip(s_headings, values))

        session.remove()
        return main.templates.TemplateResponse('profile.html', context={'request': request, 's_profile': json_s_profile,
                                                                        'role': current_user.role, 'first_name': first_name,
                                                                        'last_name': last_name, 'url': config.settings.url, 's_info_dict': s_info_dict},
                                               status_code=status.HTTP_200_OK)
    session.remove()
    raise exceptions.ForbiddenException


@router.post("/complete_admin_profile", response_class=HTMLResponse)
def add_admin_info(request: Request, response: Response, admin: schemas.AdminInfo = Depends(), db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        if len(str(admin.contact_no)) < 10 or len(str(admin.contact_no)) > 10:
            session.remove()
            return main.templates.TemplateResponse('popup.html',
                                                   context={'request': request,
                                                            'server_error': "Contact Number must be 10 digit",
                                                            'url': config.settings.url},
                                                   status_code=status.HTTP_400_BAD_REQUEST)
        new_admin = models.Admin(user_id=current_user.id, **admin.dict())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        session.remove()
        adm_update_detail = "Profile Information Added"
        return main.templates.TemplateResponse('popup.html', context={'request': request,
                                                                      'adm_update_detail': adm_update_detail,
                                                                      'url': config.settings.url},
                                               status_code=status.HTTP_201_CREATED)

    session.remove()
    raise exceptions.ForbiddenException


@router.get("/admin_profile", response_class=HTMLResponse)
def admin_profile(request: Request, response: Response, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        if not utils.check_if_profile_complete(current_user.id, current_user.role):
            session.remove()
            return RedirectResponse(url="/fill_profile_info", status_code=status.HTTP_302_FOUND)
        # Left outer join
        a_updated_profile = db.query(models.Users, models.Admin).join(models.Admin, models.Admin.user_id == models.Users.id,
                                                                      isouter=True).filter(models.Admin.user_id == current_user.id).first()
        first_name = utils.check_if_email_exists(current_user.email).firstname
        last_name = utils.check_if_email_exists(current_user.email).lastname

        a_profile = schemas.AdminAllDetails.from_orm(a_updated_profile)
        json_a_profile = jsonable_encoder(a_profile)
        a_headings = ["First Name", "Last Name", "Email", "Admin ID", "User ID", "Date of Birth", "Address", "Contact No"]
        values = []
        for k, val in json_a_profile.items():
            for k2, val2 in val.items():
                values.append(val2)
        info_dict = dict(zip(a_headings, values))
        session.remove()
        return main.templates.TemplateResponse('profile.html',
                                               context={'request': request, 'a_profile': json_a_profile,
                                                        'role': current_user.role, 'first_name': first_name,
                                                        'last_name': last_name, 'url': config.settings.url,
                                                        'info_dict': info_dict},
                                               status_code=status.HTTP_200_OK)
    session.remove()
    raise exceptions.ForbiddenException


@router.post("/complete_tutor_profile", response_class=HTMLResponse)
def add_tutor_info(request: Request, response: Response, tutor: schemas.TutorInfo = Depends(), db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'tutor':
        tutor_already_exists = utils.check_if_tutor_exists(tutor.tutor_of)
        if tutor_already_exists:
            session.remove()
            invalid_tutor_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                               detail=f"Tutor of {tutor.tutor_of.title()} already exists with us")
            return main.templates.TemplateResponse('popup.html',
                                                   context={'request': request, 'server_error': invalid_tutor_exception.detail, 'url': config.settings.url},
                                                   status_code=invalid_tutor_exception.status_code)
        if len(str(tutor.contact_no)) < 10 or len(str(tutor.contact_no)) > 10:
            session.remove()
            return main.templates.TemplateResponse('popup.html',
                                                   context={'request': request,
                                                            'server_error': "Contact Number must be 10 digit",
                                                            'url': config.settings.url},
                                                   status_code=status.HTTP_400_BAD_REQUEST)

        new_tutor = models.Tutor(user_id=current_user.id, **tutor.dict())
        db.add(new_tutor)
        db.commit()
        db.refresh(new_tutor)
        session.remove()
        tut_update_detail = "Profile Information Added"
        return main.templates.TemplateResponse('popup.html', context={'request': request,
                                                                      'tut_update_detail': tut_update_detail,
                                                                      'url': config.settings.url},
                                               status_code=status.HTTP_201_CREATED)
    session.remove()
    raise exceptions.ForbiddenException


@router.get("/tutor_profile", response_class=HTMLResponse)
def tutor_profile(request: Request, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 'tutor':
        if not utils.check_if_profile_complete(current_user.id, current_user.role):
            session.remove()
            return RedirectResponse(url="/fill_profile_info", status_code=status.HTTP_302_FOUND)
        # Left outer join
        t_updated_profile = db.query(models.Users, models.Tutor).join(models.Tutor, models.Tutor.user_id == models.Users.id,
                                                                      isouter=True).filter(models.Tutor.user_id == current_user.id).first()
        first_name = utils.check_if_email_exists(current_user.email).firstname
        last_name = utils.check_if_email_exists(current_user.email).lastname

        t_profile = schemas.TutorAllDetails.from_orm(t_updated_profile)
        json_s_profile = jsonable_encoder(t_profile)
        t_headings = ["First Name", "Last Name", "Email", "Tutor ID", "User ID", "Course Name", "Date of Birth",
                      "Address", "Contact No"]
        values = []
        for k, val in json_s_profile.items():
            for k2, val2 in val.items():
                values.append(val2)
        t_info_dict = dict(zip(t_headings, values))
        session.remove()
        return main.templates.TemplateResponse('profile.html',
                                               context={'request': request, 't_profile': t_updated_profile,
                                                        'role': current_user.role, 'first_name': first_name,
                                                        'last_name': last_name, 'url': config.settings.url,
                                                        't_info_dict': t_info_dict},
                                               status_code=status.HTTP_200_OK)
    session.remove()
    raise exceptions.ForbiddenException
