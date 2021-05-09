import sqlite3

from fastapi import APIRouter, Request, Response, status, HTTPException
from fastapi.responses import JSONResponse

d_router = APIRouter()

@d_router.on_event("startup")
async def startup():
    d_router.dbconn = sqlite3.connect("northwind.db")
    d_router.dbconn.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific

@d_router.on_event("shutdown")
async def shutdown():
    d_router.dbconn.close()

@d_router.get('/categories', status_code=status.HTTP_200_OK)
async def get_categories():
    cursor = d_router.dbconn.cursor()
    try:
        data = cursor.execute(
            "SELECT CategoryID, CategoryName FROM categories ORDER BY CategoryID"
            ).fetchall()
        return JSONResponse(
            {
                "categories": [{"id": row[0], "name": row[1]} for row in data]
            },
            status_code=status.HTTP_200_OK            
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{e}"
        )
    
@d_router.get('/customers', status_code=status.HTTP_200_OK)
async def get_customers():
    cursor = d_router.dbconn.cursor()
    try:
        data = cursor.execute(
            "SELECT CustomerID, ContactName FROM customers ORDER BY CustomerID"
            ).fetchall()
        return JSONResponse(
            {
                "customers": [{"id": row[0], "name": row[1]} for row in data]
                # "customers": data
            }, 
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{e}"
        )