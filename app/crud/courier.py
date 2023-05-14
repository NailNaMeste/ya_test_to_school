import datetime

from sqlalchemy.orm import Session

from app import models, schemas


def create_couriers(db: Session, couriers: list[schemas.CreateCourierDto]):
    objs = []

    for courier in couriers:
        create_dict = courier.dict()
        working_hours = create_dict.get("working_hours")
        obj = models.Courier(**create_dict)
        obj.workdays = [
            models.CourierWorkDay(working_hours=working_hours),
        ]
        objs.append(obj)

    db.add_all(objs)
    db.commit()
    return objs


def get_courier(db: Session, courier_id: int):
    return (
        db.query(models.Courier).filter(models.Courier.courier_id == courier_id).first()
    )


def get_couriers(db: Session, limit: int, offset: int):
    return db.query(models.Courier).offset(offset).limit(limit).all()


def get_courier_orders(
    db: Session,
    courier_id: int,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    qs = (
        db.query(models.Courier)
        .filter(models.Courier.courier_id == courier_id)
        .first()
        .orders.filter(models.Order.complete_time.between(start_date, end_date))
        .all()
    )
    return qs
