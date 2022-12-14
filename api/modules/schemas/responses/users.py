from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import List
from modules.schemas.responses.base_response import BaseResponse


class CreateUserResponse(BaseResponse):
    username: str = ""
    userid: str = ""
    email: EmailStr = None
    created_at: datetime = None


class GetUserResponse(BaseResponse):
    user: dict = {}


class GetUsersResponse(BaseResponse):
    users: List = []


class UserInDb(BaseResponse):
    hashed_password: str = ""


class GetInfoResponse(BaseResponse):
    info: dict = {}
