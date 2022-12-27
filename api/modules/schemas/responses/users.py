from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import List
from modules.schemas.responses.base_response import BaseResponse


class CreateUserResponse(BaseResponse):
    userid: str = ""


class GetUserResponse(BaseResponse):
    user: dict = {}


class GetUsersResponse(BaseResponse):
    users: List = []


class UserInDb(BaseResponse):
    hashed_password: str = ""


class GetInfoResponse(BaseResponse):
    info: dict = {}
