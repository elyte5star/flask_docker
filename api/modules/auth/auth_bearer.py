from os import path
import time
from jose import jwt
from flask_httpauth import HTTPTokenAuth
from flask import jsonify
from modules.schemas.requests.auth import JWTcredentials
from werkzeug.http import HTTP_STATUS_CODES
from modules.config.config import Config

cfg = Config().from_toml_file()

# To protect the views
security = HTTPTokenAuth(scheme="Bearer")


def error_response(status_code, message=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)


def check_token(token: str):
    if token is None:
        return None
    try:
        decoded_token = jwt.decode(token, cfg.secret_key, algorithms=[cfg.algorithm])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return None


@security.verify_token
def verify_jwt(token: str):
    return check_token(token)


@security.error_handler
def http_token_auth_error(status):
    return error_response(status)
