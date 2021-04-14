from fastapi import FastAPI
from models import HelloResp

app = FastAPI()
app.counter = 0

@app.get("/")
def root_view():
	return {"message": "Hello world!"}

@app.get('/counter')
def counter():
    app.counter += 1
    return app.counter

@app.get("/hello/{name}", response_model=HelloResp)
async def hello_name_view(name: str):
    return HelloResp(msg=f"Hello {name}")
