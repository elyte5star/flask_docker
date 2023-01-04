from pydantic import BaseModel
from modules.schemas.responses.base_response import BaseResponse
from datetime import datetime
from pydantic.types import List
from pydantic.typing import Any


class GetProductsDetailsResponse(BaseResponse):
    data: Any = None


class GetProductsResponse(BaseResponse):
    data: List = []


class GetSortResponse(GetProductsResponse):
    pass


class CreateProductResponse(BaseResponse):
    pid: str = ""
