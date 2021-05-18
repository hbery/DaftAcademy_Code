from typing import Optional
from pydantic import BaseModel, PositiveInt

class Message(BaseModel):
	message: str

class Person(BaseModel):
	name: str
	surname: str

class RegisteredPerson(BaseModel):
	id: int
	name: str
	surname: str
	register_date: str
	vaccination_date: str

class Token(BaseModel):
	token: str
 
class NewCategory(BaseModel):
	name: str

class SupplierSmall(BaseModel):
	SupplierID: PositiveInt
	CompanyName: str

	class Config:
		orm_mode = True

class CategoryData(BaseModel):
	CategoryID: PositiveInt
	CategoryName: str  

	class Config:
		orm_mode = True

class SupplierProduct(BaseModel):
	ProductID: PositiveInt
	ProductName: str
	Category: CategoryData
	Discontinued: int

	class Config:
		orm_mode = True
  
class ReturnSupplier(BaseModel):
	SupplierID: PositiveInt
	CompanyName: Optional[str]
	ContactName: Optional[str]
	ContactTitle: Optional[str]
	Address: Optional[str]
	City: Optional[str]
	PostalCode: Optional[str]
	Country: Optional[str]
	Phone: Optional[str]
	Fax: Optional[str]
	HomePage: Optional[str]

	class Config:
		orm_mode = True
  

class PostSupplier(BaseModel):
	CompanyName: str
	ContactName: Optional[str] # = "Test Contact Name"
	ContactTitle: Optional[str] # = "Unknown"
	Address: Optional[str] # = "Test Address"
	City: Optional[str] # = "Test City"
	PostalCode: Optional[str] # = "123-123"
	Country: Optional[str] # = "Unknown"
	Phone: Optional[str] # = "123-123-123"

	class Config:
		orm_mode = True

class UpdateSupplier(BaseModel):
	CompanyName: Optional[str]
	ContactName: Optional[str]
	ContactTitle: Optional[str]
	Address: Optional[str]
	City: Optional[str]
	PostalCode: Optional[str]
	Country: Optional[str]
	Phone: Optional[str]

	class Config:
		orm_mode = True
