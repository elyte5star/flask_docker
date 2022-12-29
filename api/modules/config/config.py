from pyconfs import Configuration
from pathlib import Path
from os import getenv, path

project_root = Path(__file__).parent.parent.parent
toml_path = path.join(project_root, "config.toml")
cf = Configuration.from_file(toml_path)


class Config:
    def __init__(self) -> None:
        # Initialize the config object.

        self.mongoHost: str = ""
        self.mongoPort: int = 0
        self.mongoAdminDB: str = ""
        self.mongoUsername: str = ""
        self.mongoPassword: str = ""

        # Api
        self.log_type: str = ""
        self.host_url: str = ""
        self.debug: bool = False
        self.host_port: int = 0

        # Password Hashing
        self.pwd_len: int = 0
        self.round: int = 0
        self.coding: str = ""

        # Project details
        self.name: str = ""
        self.version: str = ""
        self.description: str = ""

        # JWT params
        self.algorithm: str = ""
        self.secret_key: str = ""
        self.token_expire_min: int = 0

        # Google auth
        self.google_client_secret: str = ""
        self.google_client_id: str = ""
        # News
        self.news_api_key: str = ""

    def from_toml_file(self):
        """
        Return the config object.
        """
        self.mongoHost = cf.database.host
        self.mongoPort = cf.database.port
        self.mongoAdminDB = cf.database.admin_db
        self.mongoUsername = cf.database.user
        self.mongoPassword = cf.database.pwd

        self.log_type = cf.api.log_type
        self.host_url = cf.api.host_url
        self.debug = cf.api.debug
        self.host_port = cf.api.host_port

        self.pwd_len = cf.hash.length
        self.rounds = cf.hash.rounds
        self.coding = cf.hash.coding

        self.name = cf.app["name"]
        self.version = cf.app.version
        self.description = cf.app.description

        self.algorithm = cf.api.algorithm
        self.secret_key = cf.api.secret_key
        self.token_expire_min = cf.api.token_expire_min

        self.google_client_secret = cf.api.google_client_secret
        self.google_client_id = cf.api.google_client_id
        self.news_api_key = cf.api.news_api_key

        return self

    def from_env_file(self):
        """
        Return the config object.
        """
        print("overriding some of the settings from the environment vars")
        self.mongoHost = str(getenv("MONGODB_HOST"))
        self.mongoPort = int(getenv("MONGODB_PORT"))
        self.mongoAdminDB = str(getenv("MONGODB_DATABASE_ADMIN"))
        self.mongoUsername = str(getenv("MONGODB_AUTH_USER"))
        self.mongoPassword = str(getenv("MONGODB_AUTH_PWD"))
        self.token_expire_min = int(getenv("TOKEN_EXPIRE_MINUTES"))
        self.algorithm = str(getenv("ALGORITHM"))
        self.secret_key = str(getenv("SECRET_KEY"))
        self.google_client_secret = str(getenv("GOOGLE_CLIENT_SECRET"))
        self.google_client_id = str(getenv("GOOGLE_CLIENT_ID"))
        return self
