from fastapi import FastAPI, status, Request
from dbase import models
from routes import rec_request, user, doubt_clearing_request, auth, admin, tutor
from dbase.database import engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(rec_request.router)
app.include_router(doubt_clearing_request.router)
app.include_router(admin.router)
app.include_router(tutor.router)

templates = Jinja2Templates(directory="templates")


@app.get("/",status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
