from datetime import date

from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.templating import Jinja2Templates

from models import Token
from util import check_credentials

m_router = APIRouter()
m_router.token = ""
m_router.session = ""

templates = Jinja2Templates(directory="templates")


@m_router.get("/hello")
def send_hello(request: Request):
	return templates.TemplateResponse(
		"hello.html.j2",
		{"request": request, "today_date": date.today()}
	)


@m_router.post("/login_session", status_code=status.HTTP_201_CREATED)
def login_session(response: Response, session_token: str = Depends(check_credentials)):
	m_router.session = session_token
	response.set_cookie(key="session_token", value=session_token)
	return {"message": "Successfully Authorized"}


@m_router.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_token(token: str = Depends(check_credentials)):
	m_router.token = token
	return Token(token=token)