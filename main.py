from fastapi import FastAPI, status
from dbase import models
from routes import recrequest, user, doubtrequest, auth
from dbase.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(recrequest.router)
app.include_router(doubtrequest.router)


@app.get("/",status_code=status.HTTP_200_OK)
def home():
    return {"message": "Welcome to Request System"}





