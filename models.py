from pydantic import BaseModel


class HelloResp(BaseModel):
	msg: str