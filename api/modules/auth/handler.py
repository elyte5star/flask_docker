from modules.schemas.requests.auth import LoginDataRequest
from modules.schemas.responses.auth import TokenResponse
from typing import Optional
from modules.database.mongodb.base import Database
from jose import jwt
import bcrypt
import time
from datetime import timedelta
from flask import session


class Auth(Database):
    def login_token(self, data: LoginDataRequest) -> TokenResponse:
        user = self.get_user({"username": data.username})
        if user and self.verify_password(
            data.password, user["password"], self.cf.coding
        ):
            active = True
            admin = False
            rabbat = None

            if user["username"] == "elyte":
                admin = True
            if "agreed_discount" in user:
                rabbat = user["agreed_discount"]
            if "normal_discount" in user:
                rabbat = user["normal_discount"]
            data = {
                "userid": str(user["_id"]),
                "sub": user["username"],
                "email": user["email"],
                "admin": admin,
                "active": active,
            }
            access_token = self.create_token(
                data=data,
                expires_delta=self.time_delta(self.cf.token_expire_min),
            )
            session["user"] = {
                "username": user["username"],
                "userid": data["userid"],
                "discount": rabbat,
                "email": user["email"],
                "telephone": user["telephone"],
            }
            return TokenResponse(
                token_data={
                    "access_token": access_token,
                    "token_type": "bearer",
                    "username": user["username"],
                    "host_url": self.cf.host_url,
                },
                message=f"{user['username']} is authorized!",
            )
        return self.bad_request(
            f"User {data.username} is not authorized!Wrong Password",
        )

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        _encode = data.copy()
        if expires_delta:
            _expire = self.time_now() + expires_delta
        else:
            _expire = self.time_now() + self.time_delta(self.cf.token_expire_min)
        _encode.update({"exp": _expire})
        jwt_encode = jwt.encode(
            _encode, self.cf.secret_key, algorithm=self.cf.algorithm
        )
        return jwt_encode
