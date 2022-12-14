from pydantic import BaseModel
from datetime import datetime


class CreateOrder(BaseModel):
    pid: str
    volume: str
    unit_price: float


class ConfirmOrderRequest(BaseModel):
    email: str = ""
    telephone: str = ""
    userid: str = ""
