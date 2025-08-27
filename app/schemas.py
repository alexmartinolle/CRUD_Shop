# app/shemas.py

# Imports
# Pydantic es utilizado para la validación de datos y la creación de esquemas
from pydantic import BaseModel, EmailStr, Field

# ITEM MODEL
class ProductBase(BaseModel):
    title: str
    price: float # Price per kilogram
    description: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

# ORDER ITEM MODEL
class OrderItemBase(BaseModel):
    product_id: str
    price : float # This will be calculated: weigth * Product.price in the create order endpoint
    weight: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    class Config:
        orm_mode = True

# ORDER MODEL
class OrderBase(BaseModel):
    date: str
    total: float
    items: list[OrderItem]  # Will contain the list of items in the order

class OrderCreate(OrderBase):
    client_id: int

class Order(OrderBase):
    id: int
    class Config:
        orm_mode = True

# CLIENT MODEL
class ClientBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    direction: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=9, max_length=9)


class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    class Config:
        orm_mode = True


