from os import stat
import sqlite3
from typing import OrderedDict

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
        
        
        
        return dict(customers=[{
            "id": row["id"].strip().replace("  ", " "), 
            "name": row["name"].strip().replace("  ", " "), 
            "full_address": row["full_address"].strip().replace("  ", " ")}
        for row in data])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{e}"
        )
        
@d_router.get("/products/{pid}", status_code=status.HTTP_200_OK)
async def select_product(pid: int):
    if not isinstance(pid, int):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record identified by given id: {pid} does not exist."
        )
    
    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row
    
    products = cursor.execute("""
                              SELECT 
                                ProductID as id, 
                                ProductName as name 
                              FROM Products 
                              WHERE id = :pid""", 
                              {"pid": pid}
    ).fetchone()
    
    if products:
        return dict(id=products["id"], name=products["name"])
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record identified by given id: {pid} does not exist."
        )
        
@d_router.get("/employees", status_code=status.HTTP_200_OK)
async def get_employees(limit: int = 0, offset: int = 0, order: str = ""):
    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row
    
    accept_order = ["last_name", "first_name", "city"]
    query_string = "SELECT EmployeeID as id, LastName as last_name, FirstName as first_name, City as city FROM Employees"
    
    if order in accept_order:
        query_string += f" ORDER BY {order}"
    elif order == "":
        query_string += f" ORDER BY id"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Specified wrong order"
        )
    
    if limit != 0 and isinstance(limit, int):
        query_string += f" LIMIT {limit}"
        
    if offset != 0 and isinstance(offset, int):
        query_string += f" OFFSET {offset}"

    employees = cursor.execute(query_string).fetchall()
    
    return dict(emplyees=employees)