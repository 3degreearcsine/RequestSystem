import time
from fastapi import FastAPI, status, Request, HTTPException
from app.dbase import models, config
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


@app.exception_handler(exceptions.CredentialsException)
def credentials_exception_handler(request: Request, exc: exceptions.CredentialsException):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    response = templates.TemplateResponse("popup.html", {"request": request, "error": exception.detail,
                                                         'url': config.settings.url},
                                          status_code=exception.status_code, headers={"WWW-Authenticate": "Bearer"})
    response.delete_cookie("Authorization")
    return response


@app.exception_handler(exceptions.TokenExpiredException)
def token_expired_exception_handler(request: Request, exc: exceptions.TokenExpiredException):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session Expired")
    return templates.TemplateResponse("popup.html", {"request": request, "error": exception.detail,
                                                     'url': config.settings.url},
                                      status_code=exception.status_code, headers={"WWW-Authenticate": "Bearer"})


@app.exception_handler(exceptions.ForbiddenException)
def forbidden_exception_handler(request: Request, exc: exceptions.ForbiddenException):
    forbidden_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Forbidden")
    return templates.TemplateResponse("popup.html", {"request": request, "forbidden": forbidden_exception.detail,
                                                     'url': config.settings.url},
                                      status_code=forbidden_exception.status_code)


@app.exception_handler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_exception_handler(request: Request, exc: status.HTTP_405_METHOD_NOT_ALLOWED):
    not_allowed_exception = HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method Not Allowed")
    return templates.TemplateResponse("popup.html", {"request": request, "not_allowed": not_allowed_exception.detail},
                                      status_code=not_allowed_exception.status_code)


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def server_exception_handler(request: Request, exc: status.HTTP_500_INTERNAL_SERVER_ERROR):
    server_error = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return templates.TemplateResponse("popup.html", {"request": request, "server_error": server_error.detail},
                                      status_code=server_error.status_code)


@app.exception_handler(status.HTTP_403_FORBIDDEN)
def forbidden_exception_handler(request: Request, exc: exceptions.ForbiddenException):
    not_authenticated_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authenticated")
    return templates.TemplateResponse("popup.html", {"request": request,
                                                     "not_authenticated": not_authenticated_exception.detail,
                                                     'url': config.settings.url},
                                      status_code=not_authenticated_exception.status_code)


@app.middleware("https")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, 'url': config.settings.url})
