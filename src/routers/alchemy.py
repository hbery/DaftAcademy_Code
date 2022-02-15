import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends,
    Response
)

from sqlmodels import (
    Category,
    Supplier,
    Product,
    # t_suppliers
)
from models import (
    SupplierSmall,
    SupplierProduct,
    CategoryData,
    ReturnSupplier,
    PostSupplier,
    UpdateSupplier
)

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

a_router = APIRouter()


def get_database():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@a_router.get("/suppliers", status_code=status.HTTP_200_OK)
async def get_suppliers(db: Session = Depends(get_database)):
    suppliers = db.query(Supplier).order_by(Supplier.SupplierID).all()
    return [SupplierSmall(
                SupplierID=row.SupplierID,
                CompanyName=row.CompanyName
            )
            for row in suppliers]


@a_router.get("/suppliers/{supplier_id}", status_code=status.HTTP_200_OK)
async def get_supplier_by_id(supplier_id: int = None,
                             db: Session = Depends(get_database)):
    if not supplier_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    supplier = db.query(Supplier).filter(
                                    Supplier.SupplierID == supplier_id
                                ).first()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    return supplier


@a_router.get("/suppliers/{supplier_id}/products",
              status_code=status.HTTP_200_OK)
async def get_products_by_supplier(supplier_id: int = None,
                                   db: Session = Depends(get_database)):
    if not supplier_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    products = (db.query(Product, Category)
                .filter(Product.CategoryID == Category.CategoryID)
                .filter(Product.SupplierID == supplier_id)
                .order_by(Product.ProductID.desc())
                .all()
                )

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    return list(
        [SupplierProduct(
            ProductID=row.Product.ProductID,
            ProductName=row.Product.ProductName,
            Category=CategoryData(
                CategoryID=row.Category.CategoryID,
                CategoryName=row.Category.CategoryName
            ),
            Discontinued=row.Product.Discontinued
            ) for row in products]
    )


@a_router.post("/suppliers",
               status_code=status.HTTP_201_CREATED,
               response_model=ReturnSupplier)
async def create_supplier(nsupp: PostSupplier,
                          db: Session = Depends(get_database)):

    last_id = db.query(Supplier).order_by(Supplier.SupplierID.desc()).first()

    orm_supplier = Supplier(**nsupp.dict())
    orm_supplier.SupplierID = last_id.SupplierID + 1

    db.add(orm_supplier)
    db.flush()
    db.commit()

    return orm_supplier


@a_router.put("/suppliers/{supplier_id}",
              status_code=status.HTTP_200_OK,
              response_model=ReturnSupplier)
async def update_supplier(supplier_id: int,
                          usupp: UpdateSupplier,
                          db: Session = Depends(get_database)):
    if not supplier_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    to_update: Supplier = db.get(Supplier, supplier_id)
    if not to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    # XXX 2022-02-15 WARN: dunno what was it for; go find out
    # updict = {k: v for k, v in usupp.dict().items() if v is not None}
    # if updict:
    #     is_updated = (db.query(Supplier)
    #                     .filter(Supplier.SupplierID == supplier_id)
    #                     .update(updict, synchronize_session="fetch"))

    db.flush()
    db.commit()
    db.refresh(to_update)

    return to_update


@a_router.delete("/suppliers/{supplier_id}",
                 status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int,
                          db: Session = Depends(get_database)):
    if not supplier_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    to_delete: Supplier = db.get(Supplier, supplier_id)
    if not to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )

    db.delete(to_delete)
    db.flush()
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
