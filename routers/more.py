from requests import get
from requests.utils import dict_from_cookiejar
from datetime import date

from fastapi import APIRouter, Request, Response, status, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_route_log.log_request import LoggingRoute

from models import Token, Message
from util import check_credentials

m_router = APIRouter()
# m_router.route_class = LoggingRoute

m_router.token = None
m_router.session = None

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
	return Token(
		token=token
	)


@m_router.get("/welcome_session")
def welcome_session(request: Request, format: str = ""):
	if ("session_token" not in request.cookies.keys()):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			# detail="Not authorized"
			detail="I went to no keys"
		)
	if (request.cookies["session_token"] is None):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			# detail="Not authorized"
			detail="Session_token is None"
		)
	if (request.cookies["session_token"] != m_router.session):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			# detail="Not authorized"
			detail="Tokens dont match"
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

@m_router.delete('/logout_session', status_code=status.HTTP_302_FOUND)
def logout_session(request: Request, format: str = ""):
	if ("session_token" not in request.cookies.keys()) or (request.cookies["session_token"] is None) or (request.cookies["session_token"] != m_router.session):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized"
		)

	m_router.session_token = None

	return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)

@m_router.delete('/logout_token', status_code=status.HTTP_302_FOUND)
def logout_token(request: Request, token: str = "", format: str = ""):
	if not token or token == "" or token != m_router.token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized"
		)

	m_router.token = None

	return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@m_router.api_route('/logged_out', status_code=status.HTTP_200_OK, methods=['GET', 'DELETE'])
def logged_out(request: Request, format: str = ""):
	print(request.headers)

	if format == 'json':
		return Message(
			message="Logged out!"
		)
	elif format == 'html':
		return templates.TemplateResponse(
			"logged_out.html.j2",
			{"request": request}
		)
	else:
		return Response(
			content="Logged out!",
			media_type="text/plain"
		)