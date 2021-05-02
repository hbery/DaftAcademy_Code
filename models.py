from pydantic import BaseModel
from datetime import date

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