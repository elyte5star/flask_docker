from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class GetUserRequest(BaseModel):
    username: str = ""
