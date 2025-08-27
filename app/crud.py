# app/crud.py

# Imports
from sqlalchemy.orm import Session
from app import models, schemas

# GET PRODUCTS
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(title=product.title, price=product.price, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.title = product.title
        db_product.description = product.description
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

# GET ITEM ORDERS
def get_order_item(db: Session, order_item_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()

def get_order_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.OrderItem).offset(skip).limit(limit).all()

def create_order_item(db: Session, order_item: schemas.OrderItemCreate, order_id: int):
    product = db.query(models.Product).filter(models.Product.id == order_item.product_id).first()
    if not product:
        raise Exception("Product not found")
    order_item.price = order_item.weight * product.price
    db_order_item = models.OrderItem(
        product_id=order_item.product_id,
        order_id=order_id,
        price=order_item.price,
        weight=order_item.weight
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def delete_order_item(db: Session, order_item_id: int):
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item:
        db.delete(db_order_item)
        db.commit()
        return True
    return False

def update_order_item(db: Session, order_item_id: int, order_item: schemas.OrderItemCreate):
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item:
        if db_order_item.product_id != order_item.product_id:
            product = db.query(models.Product).filter(models.Product.id == order_item.product_id).first()
            if not product:
                raise Exception("Product not found")
            db_order_item.price = order_item.weight * product.price
        db_order_item.product_id = order_item.product_id
        db_order_item.weight = order_item.weight
        db.commit()
        db.refresh(db_order_item)
        return db_order_item
    return None

# GET ORDERS
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        client_id=order.client_id, 
        date=order.date, 
        total=order.total
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in order.items:
        create_order_item(db, item, db_order.id)
    db_order.total = sum(item.price for item in db.query(models.OrderItem).filter(models.OrderItem.order_id == db_order.id).all())
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        for item in db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all():
            db.delete(item)
        db.delete(db_order)
        db.commit()
        return True
    return False

def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.client_id = order.client_id
        db_order.date = order.date
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

# GET CLIENTS
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(
        name=client.name, 
        direction=client.direction, 
        email=client.email, 
        phone=client.phone,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        for order in db.query(models.Order).filter(models.Order.client_id == client_id).all():
            for item in db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all():
                db.delete(item)
            db.delete(order)
        db.delete(db_client)
        db.commit()
        return True
    return False

def update_client(db: Session, client_id: int, client: schemas.ClientCreate):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        db_client.name = client.name
        db_client.direction = client.direction
        db_client.email = client.email
        db_client.phone = client.phone
        db.commit()
        db.refresh(db_client)
        return db_client
    return None