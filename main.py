from fastapi import FastAPI, Body, Request, Response, status
from models import HelloResp, Person, RegisteredPerson
from hashlib import sha512
from datetime import date, timedelta

app = FastAPI()
app.counter = 0
app.id = 0

@app.get("/")
def root_view():
	"""Return default view"""

	return {"message": "Hello world!"}

@app.api_route("/method", methods=['GET', 'POST', 'PUT', 'OPTIONS', 'DELETE'])
def return_method(request: Request, response: Response):
	"""Return method used to execute the request"""
	if request.method == 'POST':
		response.status_code = status.HTTP_201_CREATED
	return {"method": f"{request.method}"}

@app.get('/counter')
def counter():
    app.counter += 1
    return app.counter

@app.get("/hello/{name}", response_model=HelloResp)
async def hello_name_view(name: str):
    return HelloResp(msg=f"Hello {name}")

@app.get('/auth')
async def authorize(response: Response, password: str = '', password_hash: str = ''):
	if password != '' and password_hash != '':
		calculated_hash = sha512(password.encode()).hexdigest()
		
		if password_hash == calculated_hash:
			response.status_code = status.HTTP_204_NO_CONTENT
			return

	response.status_code = status.HTTP_401_UNAUTHORIZED
	return

@app.post('/register', response_model=RegisteredPerson)
async def register_new_user(response: Response, person: Person):
	response.status_code = status.HTTP_201_CREATED
	today = date.today()
	vac_date = today + timedelta(days=(len(person.name) + len(person.surname)))
	app.id += 1
	return RegisteredPerson(
		id=app.id, 
		name=person.name, 
		surname=person.surname, 
		register_date=today.strftime("%Y-%m-%d"), 
		vaccination_date=vac_date.strftime("%Y-%m-%d")
		)