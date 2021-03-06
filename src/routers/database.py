from models import NewCategory
import sqlite3

from fastapi import (
    APIRouter,
    status,
    HTTPException
)

from models import NewCategory

d_router = APIRouter()


@d_router.on_event("startup")
async def startup():
    d_router.dbconn = sqlite3.connect("northwind.db")
    # northwind specific
    d_router.dbconn.text_factory = lambda b: b.decode(errors="ignore")


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
                CategoryID AS id,
                CategoryName As name
            FROM Categories
            ORDER BY id;"""
        ).fetchall()

        return dict(categories=data)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )


@d_router.get('/customers', status_code=status.HTTP_200_OK)
async def get_customers():
    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row
    try:
        data = cursor.execute(
            """SELECT
                CustomerID AS id,
                COALESCE(CompanyName, '') AS name,
                (COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '')
                 || ' ' || COALESCE(City, '') || ' '
                 || COALESCE(Country, '')) AS full_address
            FROM Customers
            ORDER BY UPPER(id);"""
        ).fetchall()

        return dict(customers=data)

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
            detail=f"Record identified by given id: {pid} does not exist in Products table."
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
            detail=f"""Record identified by given id: {pid}
                       does not exist in Products table."""
        )


@d_router.get("/employees", status_code=status.HTTP_200_OK)
async def get_employees(limit: int = 0, offset: int = 0, order: str = ""):
    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row

    accept_order = ["last_name", "first_name", "city"]
    query_string = """SELECT EmployeeID as id,
                             LastName as last_name,
                             FirstName as first_name,
                             City as city
                      FROM Employees;"""

    if order in accept_order:
        query_string += f" ORDER BY {order}"
    elif order == "":
        query_string += " ORDER BY id"
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

    return dict(employees=employees)


@d_router.get('/products_extended', status_code=status.HTTP_200_OK)
async def get_products_ext():
    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row
    data = cursor.execute("""
                        SELECT
                            p.ProductID as id,
                            p.ProductName as name,
                            (SELECT c.CategoryName
                             FROM Categories as c
                             WHERE c.CategoryID = p.CategoryID) as category,
                            (SELECT s.CompanyName
                             FROM Suppliers as s
                             WHERE s.SupplierID = p.SupplierID) as supplier
                        FROM Products as p
                        ORDER BY id;"""
                          ).fetchall()

    return dict(products_extended=data)


@d_router.get('/products/{pid}/orders')
async def get_product_orders(pid: int):
    if not isinstance(pid, int):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Record identified by given id: {pid}
                       does not exist in Products table."""
        )

    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row

    data = cursor.execute("""
                        SELECT
                            od.OrderID AS id,
                            (select c.CompanyName
                             from Customers as c
                             where c.CustomerID = o.CustomerID ) AS customer,
                            od.Quantity AS quantity,
                            ROUND(((od.UnitPrice * od.Quantity)
                                   - (od.Discount
                                      * (od.Quantity * od.UnitPrice))), 2)
                            AS total_price
                        FROM 'Order Details' AS od
                        JOIN orders AS o ON o.OrderID = od.OrderID
                        JOIN Products AS p ON od.ProductID = p.ProductID
                        WHERE od.ProductID = :pid;
                        """,
                          {"pid": pid}
                          ).fetchall()

    if data:
        return dict(orders=data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record identified by given id: {pid} does not exist in Products table."
        )


@d_router.post('/categories', status_code=status.HTTP_201_CREATED)
async def create_new_category(new_category: NewCategory):
    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row

    data = cursor.execute("""
                        INSERT INTO Categories
                            (CategoryName)
                        VALUES
                            (:name)
                        """,
                          {"name": new_category.name}
                          )
    d_router.dbconn.commit()

    return dict(id=data.lastrowid, name=new_category.name)


@d_router.put("/categories/{cid}", status_code=status.HTTP_200_OK)
async def upadate_category(cid: int, new_category: NewCategory):
    if not isinstance(cid, int):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Record identified by given id: {cid}
                       does not exist in Categories table."""
        )

    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row

    cursor.execute("""
                   UPDATE Categories
                       SET CategoryName = :new_name WHERE CategoryID = :id
                   """,
                   {"new_name": new_category.name, "id": cid}
                   )
    d_router.dbconn.commit()

    data = cursor.execute("""
                        SELECT
                            CategoryID AS id,
                            CategoryName AS name
                        FROM Categories
                        WHERE id = :id
                        """,
                          {"id": cid}
                          ).fetchone()

    if data:
        return dict(id=data["id"], name=new_category.name)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Record identified by given id: {cid}
                       does not exist in Categories table."""
        )


@d_router.delete('/categories/{cid}', status_code=status.HTTP_200_OK)
async def delete_category(cid: int):
    if not isinstance(cid, int):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Record identified by given id: {cid}
                       does not exist in Categories table."""
        )

    cursor = d_router.dbconn.cursor()
    cursor.row_factory = sqlite3.Row

    check = cursor.execute("""
                        SELECT
                            CategoryID AS id,
                            CategoryName AS name
                        FROM Categories
                        WHERE id = :id
                          """,
                           {"id": cid}
                           ).fetchone()

    if check:
        data = cursor.execute("""
                            DELETE FROM Categories
                            WHERE CategoryID = :id
                                """,
                              {"id": cid}
                              )
        d_router.dbconn.commit()

        return dict(deleted=data.rowcount)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Record identified by given id: {cid}
                       does not exist in Categories table."""
        )
