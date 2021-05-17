import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from fastapi import (
    APIRouter, 
    status, 
    HTTPException,
    Depends
)

from sqlmodels import (
    Category, 
    Supplier, 
    Product
)
from models import (
    SupplierProduct, 
    SupplierSmall, 
    SupplierProduct,
    CategoryData
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
    suppliers = db.query(Supplier).all()
    return list([SupplierSmall(SupplierID=row.SupplierID, CompanyName=row.CompanyName) for row in suppliers])


@a_router.get("/suppliers/{supplier_id}", status_code=status.HTTP_200_OK)
async def get_supplier_by_id(supplier_id: int = None, db: Session = Depends(get_database)):
    if not supplier_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )
    
    supplier = db.query(Supplier).filter(Supplier.SupplierID == supplier_id).first()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )
    
    return supplier

@a_router.get("/suppliers/{supplier_id}/products", status_code=status.HTTP_200_OK)
async def get_products_by_supplier(supplier_id: int = None, db: Session = Depends(get_database)):
    if not supplier_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found"
        )
    
    products = ( db.query(Product, Category)
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
        [ SupplierProduct(
            ProductID=row.Product.ProductID, 
            ProductName=row.Product.ProductName, 
            Category=CategoryData(
                CategoryID=row.Category.CategoryID,
                CategoryName=row.Category.CategoryName
            ),
            Discontinued=row.Product.Discontinued
            ) for row in products]
    )