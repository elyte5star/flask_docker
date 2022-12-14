from pydantic.typing import Any
from modules.schemas.responses.base_response import BaseResponse


class TokenResponse(BaseResponse):
    token_data: Any = None
