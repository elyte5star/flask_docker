from pydantic import BaseModel


class GetProductDetailsRequest(BaseModel):
    pid: str
    price: str


class CreateProductRequest(BaseModel):
    name: str
    location: str
    description: str
    details: str
    image: str
    price: float
    category: str
