from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas import authentication
from fastapi import Request
from typing import Union, Any

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# , credentials_exception
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = int(payload.get("sub"))
        if id is None:
            raise credentials_exception
        token_data = authentication.TokenData(id=id)
    except JWTError:
        raise credentials_exception
 
    return token_data


def is_admin_authenticated(request: Request):

    # token = request.headers.get("Authorization", None)
    token = request.cookies.get('admin_session_cookie')
    # print(token)

    if token is not None:

        try:
            encoded_jwt = token.split(" ")[1]


            payload = jwt.decode(
                encoded_jwt,
                SECRET_KEY,
                ALGORITHM
            )
            # print(payload)

            return {
                "flag": True,
                "message": "Decode successfully",
                "payload": payload
            }

        except jwt.ExpiredSignatureError:

            return {"flag": False, "message": "token expired"}

    return {"flag": False, "message": "admin cookie is not present"}    


def create_access_token_admin(subject: Union[str, Any], expires_delta: int = None) -> str:

    # print(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=30)
    # print(expires_delta)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt