from fastapi import FastAPI, status, Request, Response
from app.dbase import models
from app.routes import admin, auth, user, doubt_clearing_request, rec_request, tutor
from app.dbase.database import engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app import exceptions

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(rec_request.router)
app.include_router(doubt_clearing_request.router)
app.include_router(admin.router)
app.include_router(tutor.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.exception_handler(exceptions.ForbiddenException)
def forbidden_exception_handler():
    error = "Access Forbidden"
    Response.status_code = status.HTTP_403_FORBIDDEN
    return error


@app.get("/",status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
