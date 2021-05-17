from pydantic import BaseModel, PositiveInt
from pydantic.fields import T

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