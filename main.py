from fastapi import FastAPI
from fastapi_route_log.log_request import LoggingRoute
from routers import simple, more

app = FastAPI()
# app.router.route_class = LoggingRoute

app.include_router(
	simple.s_router,
	tags=["simple_endpoints"]
)
app.include_router(
	more.m_router,
	tags=["more_endpoints"]
)

@app.get("/")
def root_view():
	"""Return default view"""

	return {"message": "Hello world!"}
	