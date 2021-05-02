from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import date

m_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@m_router.get("/hello")
def send_hello(request: Request):
	return templates.TemplateResponse(
		"hello.html.j2",
		{"request": request, "today_date": date.today()}
	)