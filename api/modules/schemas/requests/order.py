from pydantic import BaseModel


class CreateOrder(BaseModel):
    pid: str
    volume: str
    unit_price: float


class ConfirmOrderRequest(BaseModel):
    email: str = ""
    telephone: str = ""
    userid: str = ""
    pid: str = ""



