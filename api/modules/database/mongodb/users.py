from modules.schemas.requests.users import CreateUserRequest, GetUserRequest
from modules.schemas.responses.users import (
    CreateUserResponse,
    GetUserResponse,
    GetUsersResponse,
)
from modules.database.mongodb.base import Database
from modules.auth.auth_bearer import security


class Users(Database):
    def _create_user(self, user_data: CreateUserRequest) -> CreateUserResponse:
        user_dict = self.admin_db.users.find_one(
            {
                "$or": [
                    {"email": user_data.email},
                    {"username": user_data.username},
                ]
            }
        )
        if user_dict:
            return self.bad_request(
                f"User with {user_data.email}/{user_data.username} already registered!"
            )
        payload = {
            "username": user_data.username,
            "email": user_data.email,
            "password": self.hash_password(
                user_data.password, self.cf.rounds, self.cf.coding
            ),
            "created_at": self.time_now(),
            "admin": False,
            "active": True,
            "normal_discount": 0.05,
            "telephone": user_data.telephone,
        }

        result = self.admin_db.users.insert_one(payload)
        return CreateUserResponse(
            userid=str(result.inserted_id),
            message=f"User with {user_data.email}/{user_data.username} created!",
        )

    @security.login_required
    def get_users(self) -> GetUsersResponse:
        cursor = self.admin_db.users.find({}, {"password": 0, "active": 0, "admin": 0})
        if cursor:
            user_list = []
            for user in cursor:
                user["userid"] = str(user.pop("_id"))
                user_list.append(user)
            res = {"users": user_list, "num_users": len(user_list)}
            return res
        return self.bad_request("No users found")

    @security.login_required
    def _get_user(self, data: GetUserRequest) -> GetUserResponse:
        user_dict = self.get_user({"username": data.username})
        if user_dict is None:
            return self.bad_request("User not found")
        user_dict["userid"] = str(user_dict.pop("_id"))
        for e in ["password", "active", "admin"]:
            user_dict.pop(e)
        response = {
            "user": user_dict,
            "userid": user_dict["userid"],
        }
        return response
