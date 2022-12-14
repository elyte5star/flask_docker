from datetime import datetime, timedelta
import time
import string, random
import uuid
from typing import Optional
import bcrypt
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from pymongo import MongoClient, errors
from jose import jwt
from typing import Optional


class Database(object):

    connection = None

    def __init__(self, cf):
        if Database.connection is None:
            try:
                print("Attempting to connect to mongo database server!!")
                Database.connection = MongoClient(
                    host=cf.mongoHost,
                    username=cf.mongoUsername,
                    password=cf.mongoPassword,
                    authSource=cf.mongoAdminDB,
                )
            except errors.ServerSelectionTimeoutError as error:
                print("Error: Connection not established {}".format(error))
            else:
                print("[+] Mongo Database connected!")

        self.cf = cf
        self.client = Database.connection
        self.admin_db = self.client[self.cf.mongoAdminDB]

    def get_user(self, user_dict: dict) -> Optional[dict]:
        return self.admin_db.users.find_one(user_dict)

    def time_now(self) -> datetime:
        return datetime.utcnow()

    def get_indent(self):
        return str(uuid.uuid4())

    def get_user_string(self, stringLength: int = 32) -> str:
        letters = string.ascii_lowercase + "0123456789" + string.ascii_uppercase
        return "".join(random.choice(letters) for i in range(stringLength))

    def time_delta(self, min: int) -> timedelta:
        return timedelta(minutes=min)

    def verify_password(
        self, plain_password: str, hashed_password: str, coding: str
    ) -> bool:
        if bcrypt.checkpw(
            plain_password.encode(coding), hashed_password.encode(coding)
        ):
            return True
        return False

    def hash_password(self, password: str, rounds: int, coding: str) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode(coding), bcrypt.gensalt(rounds=rounds)
        ).decode(coding)
        return hashed_password

    def error_response(self, status_code, message=None):
        payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
        if message:
            payload["message"] = message
        response = jsonify(payload)
        response.status_code = status_code
        return response

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

    def bad_request(self, message):
        return self.error_response(400, message)
