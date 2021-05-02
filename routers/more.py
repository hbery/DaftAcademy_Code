from requests import get
from requests.utils import dict_from_cookiejar
from datetime import date
from collections import deque

from fastapi import APIRouter, Request, Response, status, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_route_log.log_request import LoggingRoute

from models import Token, Message
from util import check_credentials

m_router = APIRouter()
# m_router.route_class = LoggingRoute

m_router.tokens = []
m_router.sessions = []

templates = Jinja2Templates(directory="templates")


@m_router.get("/hello")
def send_hello(request: Request):
	return templates.TemplateResponse(
		"hello.html.j2",
		{"request": request, "today_date": date.today()}
	)

@m_router.get('/clear', status_code=status.HTTP_202_ACCEPTED)
def clear_tokens():
	m_router.sessions.clear()
	m_router.tokens.clear()

	return Message(
		message="done"
	)


@m_router.post("/login_session", status_code=status.HTTP_201_CREATED)
def login_session(response: Response, session_token: str = Depends(check_credentials)):
	
	if len(m_router.sessions) >= 3:
		m_router.sessions.pop(0)
	m_router.sessions.append(session_token)

	response.set_cookie(key="session_token", value=session_token)
	return {"message": "Successfully Authorized"}


@m_router.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_token(token: str = Depends(check_credentials)):
	
	if len(m_router.tokens) >= 3:
		m_router.tokens.pop(0)
	m_router.tokens.append(token)
	
	return Token(
		token=token
	)


@m_router.get("/welcome_session")
def welcome_session(request: Request, format: str = ""):
	if ("session_token" not in request.cookies.keys()) or (request.cookies["session_token"] is None) or (request.cookies["session_token"] not in m_router.sessions):
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


@m_router.get("/welcome_token")
def welcome_token(request: Request, token: str = "", format: str = ""):
	if (not token) or (token == "") or (token not in m_router.tokens):
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
	if ("session_token" not in request.cookies.keys()) or (request.cookies["session_token"] is None) or (request.cookies["session_token"] not in m_router.sessions):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized"
		)
	
	m_router.sessions.remove(request.cookies["session_token"])

	return RedirectResponse(
		url=f"/logged_out?format={format}", 
		status_code=302
)

@m_router.delete('/logout_token', status_code=status.HTTP_302_FOUND)
def logout_token(request: Request, token: str = "", format: str = ""):
	if (not token) or (token == "") or (token not in m_router.tokens):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized"
		)

	m_router.tokens.remove(token)

	return RedirectResponse(
		url=f"/logged_out?format={format}", 
		status_code=302
	)


@m_router.api_route('/logged_out', status_code=status.HTTP_200_OK, methods=['GET', 'DELETE'])
def logged_out(request: Request, format: str = ""):

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