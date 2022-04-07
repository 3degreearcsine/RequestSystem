from fastapi import FastAPI, status
from dbase import models
from routes import rec_request, user, doubt_clearing_request, auth
from dbase.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(rec_request.router)
app.include_router(doubt_clearing_request.router)


@app.get("/",status_code=status.HTTP_200_OK)
def home():
    return {"message": "Welcome to Request System"}





