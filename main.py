from fastapi import FastAPI, status
from dbase import models
from routes import rec_request, user, doubt_clearing_request, auth, admin, tutor
from dbase.database import engine
from fastapi.responses import HTMLResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(rec_request.router)
app.include_router(doubt_clearing_request.router)
app.include_router(admin.router)
app.include_router(tutor.router)


@app.get("/",status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Request System</title>
            <style>
            .button{
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            }
            .button1{background-color: #4CAf50;}
            .button2{background-color: #008CBA;}
            </style>            
        </head>
        <body>
            <h1>Welcome to the request System</h1>
            <h2> Please Register if your are a new user or Login if you are existing user</h2>
            <button class="button button1" onclick="location.href='https://reqsys.azurewebsites.net/login';">Login</button><br>
            <button class="button button2" onclick="location.href='https://reqsys.azurewebsites.net/register';">Register</button>
        </body>
    <html>
    """






