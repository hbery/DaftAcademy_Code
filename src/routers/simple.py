from fastapi import (
    APIRouter,
    Request,
    Response,
    status
)

from models import (
    Message,
    Person,
    RegisteredPerson
)
from util import calculate_names_length

from hashlib import sha512
from datetime import date, timedelta

s_router = APIRouter()


s_router.counter = 0
s_router.id = 0
s_router.patients = []


@s_router.api_route("/method",
                    methods=['GET', 'POST', 'PUT', 'OPTIONS', 'DELETE'])
def return_method(request: Request, response: Response):
    """Return method used to execute the request"""
    if request.method == 'POST':
        response.status_code = status.HTTP_201_CREATED
    return {"method": f"{request.method}"}


@s_router.get('/counter')
def counter():
    s_router.counter += 1
    return s_router.counter


@s_router.get("/hello/{name}", response_model=Message)
async def hello_name_view(name: str):
    return Message(message=f"Hello {name}")


@s_router.get('/auth')
async def authorize(response: Response,
                    password: str = '',
                    password_hash: str = ''):
    if password != '' and password_hash != '':
        calculated_hash = sha512(password.encode()).hexdigest()

        if password_hash == calculated_hash:
            response.status_code = status.HTTP_204_NO_CONTENT
            return

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return


@s_router.post('/register',
               response_model=RegisteredPerson,
               status_code=status.HTTP_201_CREATED)
async def register_new_user(response: Response, person: Person):
    today = date.today()
    vac_date = today + timedelta(
        days=calculate_names_length(person.name, person.surname))
    s_router.id += 1
    patient = RegisteredPerson(
        id=s_router.id,
        name=person.name,
        surname=person.surname,
        register_date=today.strftime("%Y-%m-%d"),
        vaccination_date=vac_date.strftime("%Y-%m-%d")
        )

    s_router.patients.append(patient)
    return patient


@s_router.get('/patient/{patient_id}',
              response_model=RegisteredPerson,
              status_code=status.HTTP_200_OK)
async def get_patient(response: Response, patient_id: int):
    if patient_id < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return

    if patient_id not in [patient.id for patient in s_router.patients]:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return [person for person in s_router.patients
            if person.id == patient_id][0]
