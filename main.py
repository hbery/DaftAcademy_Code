from fastapi import FastAPI, Request, Response, status
from fastapi_route_log.log_request import LoggingRoute

from models import HelloResp, Person, RegisteredPerson
from util import calculate_names_length

from hashlib import sha512
from datetime import date, timedelta

app = FastAPI()
# app.router.route_class = LoggingRoute

app.counter = 0
app.id = 0
app.patients = []

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

@app.post('/register', response_model=RegisteredPerson, status_code=status.HTTP_201_CREATED)
async def register_new_user(response: Response, person: Person):
	today = date.today()
	vac_date = today + timedelta(days=calculate_names_length(person.name, person.surname))
	app.id += 1
	patient = RegisteredPerson(
		id=app.id, 
		name=person.name, 
		surname=person.surname, 
		register_date=today.strftime("%Y-%m-%d"), 
		vaccination_date=vac_date.strftime("%Y-%m-%d")
		)

	app.patients.append(patient)
	return patient

@app.get('/patient/{patient_id}', response_model=RegisteredPerson, status_code=status.HTTP_200_OK)
async def get_patient(response: Response, patient_id: int):
	if patient_id < 1:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return
	
	if patient_id not in [patient.id for patient in app.patients]:
		response.status_code = status.HTTP_404_NOT_FOUND
		return

	return [person for person in app.patients if person.id == patient_id][0]
	