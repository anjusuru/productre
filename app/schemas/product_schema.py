from datetime import datetime

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    brand: str
    price: float
    quantity: int
    category: str


# Properties to receive on item creation
class CreateProduct(ProductBase):
    pass


# Properties to receive on item update
class UpdateProduct(ProductBase):
    pass


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    pass


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    pass
