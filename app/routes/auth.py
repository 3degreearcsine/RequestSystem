from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, oauth2, utils, main
from app.dbase import models, database

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    token = request.cookies.get("Authorization")
    print(token)
    if token:
        updated_token = token.removesuffix('Bearer ')
        print(updated_token)
        token_exists = utils.check_if_blacklisted(updated_token)
        print(token_exists)
        if not token_exists:
            # return RedirectResponse(url="/logout", status_code=status.HTTP_200_OK)
            return main.templates.TemplateResponse('popup.html', context={'request': request, 'not_logged_out': 'Please logout to continue'}, status_code=status.HTTP_403_FORBIDDEN)
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username.lower()).first()
    if not user:
        invalid_username_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        return main.templates.TemplateResponse('popup.html', context={'request': request, 'error': invalid_username_exception.detail}, status_code=invalid_username_exception.status_code)
    if not utils.verfiy(user_credentials.password, user.password):
        invalid_password_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        return main.templates.TemplateResponse('popup.html', context={'request': request, 'error': invalid_password_exception.detail}, status_code=invalid_password_exception.status_code)
    access_token = oauth2.create_access_token(data={"user_id": user.id, "user_email": user.email.lower(), "user_role": user.role.lower()})

    if user.role =='student':
        response = RedirectResponse(url="/student_profile", status_code=status.HTTP_302_FOUND)
    elif user.role == 'tutor':
        response = RedirectResponse(url="/tutor_profile", status_code=status.HTTP_302_FOUND)
    else:
        response = RedirectResponse(url="/tutor_profile", status_code=status.HTTP_302_FOUND)

    response.set_cookie("Authorization", value=f"Bearer {access_token}", httponly=True)
    return response


@router.post("/logout")
def logout(request: Request, token: str = Depends(oauth2.get_user_token), current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    l_out = models.BlackListedTokens(token=token, email=current_user.email.lower())
    db.add(l_out)
    db.commit()
    db.refresh(l_out)
    database.session.remove()
    response = main.templates.TemplateResponse('popup.html', context={'request': request, 'detail': "Logout Successful"}, status_code=status.HTTP_200_OK)
    response.delete_cookie("Authorization")
    return response



