from fastapi import FastAPI, Request, Response, status
from models import HelloResp
from hashlib import sha512

app = FastAPI()
app.counter = 0

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
