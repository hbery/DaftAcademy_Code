from requests.utils import dict_from_cookiejar
from datetime import date

from fastapi import APIRouter, Request, Response, status, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates

from models import Token, Message
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


@m_router.get("/welcome_session")
def welcome_session(request: Request, format: str = ""):
	print(request.cookies.keys())
	if ("session_token" not in request.cookies.keys()):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized"
			)

	if (request.cookies["session_token"] == "") or (request.cookies["session_token"] != m_router.session):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized"
			)

	if format == 'json':
		return Message(message="Welcome!")
	elif format == 'html':
		return templates.TemplateResponse(
			"welcome.html.j2",
			{"request": request}
		)
	else:
		return Response(content="Welcome!", media_type="text/plain")


@m_router.get("/welcome_token")
def welcome_token(request: Request, token: str = "", format: str = ""):
	if not token or token == "" or token != m_router.token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized"
			)

	if format == 'json':
		return Message(
			message="Welcome!"
		)
	elif format == 'html':
		return templates.TemplateResponse(
			"welcome.html.j2",
			{"request": request}
		)
	else:
		return Response(
			content="Welcome!",
			media_type="text/plain"
		)