from pydantic import BaseModel, Extra
from datetime import timedelta


class LoginDataRequest(BaseModel):
    username: str
    password: str


class JWTcredentials(BaseModel):
    userid: str
    email: str
    username: str
    admin: bool
    active: bool
    exp: timedelta
    access_token: str
