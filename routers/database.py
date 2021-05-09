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
    cursor.row_factory = sqlite3.Row
    try:
        data = cursor.execute(
            """SELECT 
                CategoryID as id, 
                CategoryName as name 
            FROM Categories 
            ORDER BY id"""
        ).fetchall()
        
        return dict(categories=data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{e}"
        )
    
@d_router.get('/customers',status_code=status.HTTP_200_OK)
async def get_customers():
    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row
    try:
        data = cursor.execute(
            """SELECT 
                CustomerID as id, 
                COALESCE(CompanyName, '') as name, 
                (COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '')) as full_address 
            FROM Customers 
            ORDER BY id"""
        ).fetchall()
        
        return dict(customers=data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{e}"
        )
        
@d_router.get("/products/{int: id}", status_code=status.HTTP_200_OK)
async def products(id: int):
    if not isinstance(id, int):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record identified by given id: {id} does not exist."
        )
    
    cursor = d_router.db_conn.cursor()
    cursor.row_factory = sqlite3.Row
    
    products = cursor.execute("""
                              SELECT 
                                ProductID as id, 
                                ProductName as name 
                              FROM Products 
                              WHERE id = :pid""", 
                              {"pid": id}
    ).fetchone()
    
    if products:
        return dict(id=products["id"], name=products["name"])
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record identified by given id: {id} does not exist."
        )