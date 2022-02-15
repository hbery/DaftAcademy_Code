from fastapi import FastAPI
from routers import simple, more, database, alchemy

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
app.include_router(
    database.d_router,
    tags=["sqlite_endpoints"]
)

app.include_router(
    alchemy.a_router,
    tags=["postgres_endpoints"]
)


@app.get("/")
def root_view():
    """Return default view"""

    return {"message": "Hello world!"}
