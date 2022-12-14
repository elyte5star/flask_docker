from flask import Blueprint
from modules.schemas.requests.users import CreateUserRequest, GetUserRequest
from modules.schemas.responses.users import (
    CreateUserResponse,
    GetUserResponse,
    GetUsersResponse,
)

from flask_pydantic import validate

users_bp = Blueprint("users_bp", __name__, url_prefix="")


@users_bp.route("/signup", methods=["POST"])
@validate()
def create_user(body: CreateUserRequest) -> CreateUserResponse:
    return handler_user._create_user(
        CreateUserRequest(
            username=body.username,
            email=body.email,
            password=body.password,
            telephone=body.telephone,
        )
    )


@users_bp.route("/all", methods=["GET"])
@validate()
def get_users() -> GetUsersResponse:
    return handler_user.get_users()


@users_bp.route("/one/<username>", methods=["GET"])
@validate()
def get_user(username: str) -> GetUserResponse:
    return handler_user._get_user(GetUserRequest(username=username))
