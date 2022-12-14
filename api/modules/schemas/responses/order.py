from datetime import datetime
from modules.schemas.responses.base_response import BaseResponse
from pydantic.types import List


class CreateOrderResponse(BaseResponse):
    pid: str
    userid: str
    volume: str
    created_at: datetime
    sale_price: float


class GetOrderResponse(BaseResponse):
    orders: List = []


class ConfirmOrderResponse(BaseResponse):
    pass
