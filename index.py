__doc__ = "main process"

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")


@app.get("/", response_class=HTMLResponse)
def login(request: Request, error:str = None):
    """login page"""
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login")
async def do_login(request: Request, email:str = Form(...), password:str = Form(...)) :
    """login action """
    # 로그인 처리 로직

    user = db.get_user_by_email(email)
    if not user:
        return login(request, error='User email not found!!')
    valid = db.verify_password(password, user['password'])

    if valid:
        return templates.TemplateResponse('index.html', {"request":request})
    return login(request, error="email/password not match!!")

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    """main page"""
    return templates.TemplateResponse("index.html", {"request": request})
