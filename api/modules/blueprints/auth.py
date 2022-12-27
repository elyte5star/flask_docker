from flask import Blueprint, request
from modules.schemas.requests.auth import LoginDataRequest, GoogleLoginDataRequest
from modules.schemas.responses.auth import TokenResponse
from flask_pydantic import validate

auth_bp = Blueprint("auth_bp", __name__, url_prefix="")


@auth_bp.route("/get_token", methods=["POST"])
@validate()
def token(body: LoginDataRequest) -> TokenResponse:
    return handler_auth.login_token(
        LoginDataRequest(username=body.username, password=body.password)
    )


@auth_bp.route("/google", methods=["POST"])
@validate()
def google_token(body: GoogleLoginDataRequest) -> TokenResponse:
    return handler_auth.google_auth(
        GoogleLoginDataRequest(username=body.username, email=body.email)
    )
