from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import my_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme), ):

    id = my_token.verify_token(data)

    return id
