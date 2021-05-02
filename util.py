import re
import hashlib
from time import time_ns
from secrets import compare_digest

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

auth = HTTPBasic()
search = re.compile(r'[^\W\d]', re.UNICODE)

def calculate_names_length(*args, **kwargs):
	length = 0
	for name in args:
		length += len(search.findall(name))

	return length


def check_credentials(credentials: HTTPBasicCredentials = Depends(auth)) -> str:
	valid_user = compare_digest(credentials.username, "4dm1n")
	valid_pass = compare_digest(credentials.password, "NotSoSecurePa$$")

	if not (valid_user and valid_pass):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Basic"},
		)

	return hashlib.sha512(f"{credentials.password}::{credentials.username}-{time_ns()}".encode('utf-8')).hexdigest()


if __name__ == "__main__":
    print(calculate_names_length('niańka', "parówa123&*(*(&^% -"))