from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app import models, schemas


def create_orders(db: Session, orders: list[schemas.CreateOrderDto]):
    objs = []
    for order in orders:
        objs.append(models.Order(**order.dict()))

    db.add_all(objs)
    db.commit()
    return objs


def get_orders(db, limit: int, offset: int):
    return db.query(models.Order).limit(limit).offset(offset).all()


def get_order(db: Session, order_id: int) -> schemas.OrderDto:
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()
