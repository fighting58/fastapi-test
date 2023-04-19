from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/template")


@app.get("/", response_class=HTMLResponse)
def login(request: Request, error:str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login")
async def do_login(request: Request):
    # 로그인 처리 로직
    form = await request.form()
    email = form.get("email")
    password = form.get("password")

    user = db.get_user_by_email(email)
    if not user:
        return login(request, error='User email not found!!')
    valid = db.verify_password(password, user['password'])

    if valid:
        return templates.TemplateResponse('index.html', {"request":request})
    return login(request, error="email/password not match!!")

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
