from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

app = FastAPI()
templates = Jinja2Templates(directory="./static/template")

@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def login_post(request: Request, response: Response, email: str = Form(...), password: str = Form(...)):
    # 로그인 처리 로직
    if email == "user@example.com" and password == "password":
        response.status_code = HTTP_302_FOUND
        response.headers["Location"] = "/index"
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password"})

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})