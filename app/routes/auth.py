from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, oauth2, utils, main
from app.dbase import models, database

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token, response_class=HTMLResponse)
# @router.post("/login", response_model=schemas.Token)
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    database.session.remove()
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        invalid_username_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        return main.templates.TemplateResponse('login.html', context={'request': request, 'error': invalid_username_exception.detail})
    if not utils.verfiy(user_credentials.password, user.password):
        # invalid_password_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        invalid_password_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        return main.templates.TemplateResponse('login.html', context={'request': request, 'error': invalid_password_exception.detail})
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id, "user_email": user.email, "user_role": user.role})
    # return {"access_token": access_token, "token_type": "bearer"}
    # response = {"access_token": access_token, "token_type": "bearer"}
    # return main.templates.TemplateResponse('login.html', context={"request": request})
    # return main.templates.TemplateResponse('login.html', context={"request": request, "access_token": access_token, "token_type": "bearer", 'role': user.role}, '})
    return main.templates.TemplateResponse('login.html', context={"request": request, "access_token": access_token, "token_type": "bearer", 'role': user.role})


@router.post("/logout",status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2.get_user_token),
           current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    l_out = models.BlackListedTokens(token=token, email=current_user.email)
    db.add(l_out)
    db.commit()
    db.refresh(l_out)
    database.session.remove()
    return {
        "detail": "User logged out successfully."
    }



