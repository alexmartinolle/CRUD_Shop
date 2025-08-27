# app/models.py

# Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import base

# PRODUCT MODEL
class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Integer, index=True) # Price per kilogram
    description = Column(String)
    order_items = relationship("OrderItem", back_populates="product")


# ORDER ITEM MODEL
class OrderItem(base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    price = Column(Integer) # This will be calculated: weigth * Product.price in the create order endpoint
    weight = Column(Integer)
    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="items")

# ORDER MODEL
class Order(base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    date = Column(String, index=True)
    total = Column(Integer)
    items = relationship("OrderItem", back_populates="order")
    client = relationship("Client", back_populates="orders")

# CLIENT MODEL
class Client(base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    direction = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    hashed_password = Column(String)
    orders = relationship("Order", back_populates="client")