from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, oauth2, utils
from app.dbase import models, database

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verfiy(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id, "user_email": user.email, "user_role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

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



