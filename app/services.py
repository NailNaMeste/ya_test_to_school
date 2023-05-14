import datetime
from sqlalchemy.orm import Session

from app import crud, schemas


def complete_order(db: Session, complete_data: list[schemas.CompleteOrderDto]):
    orders = []

    for item in complete_data:
        order_obj = crud.get_order(db, item.order_id)
        if order_obj.courier_id or order_obj.complete_time:
            return
        if not crud.get_courier(db, item.courier_id):
            return
        order_obj.courier_id = item.courier_id
        order_obj.complete_time = item.complete_time
        orders.append(order_obj)
    db.commit()

    return orders


# 2023-01-20
def get_courier_meta_info(db: Session, courier_id: int, start_date: str, end_date: str):
    earnings = 0
    earnings_enum = {"FOOT": 2, "BIKE": 3, "AUTO": 4}
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    orders = crud.get_courier_orders(db, courier_id, start_date, end_date)
    for order in orders:
        earnings += order.cost * earnings_enum.get(order.courier.courier_type.value)

    ratings_enum = {"FOOT": 3, "BIKE": 2, "AUTO": 1}
    courier = crud.get_courier(db, courier_id)

    orders_count = len(orders)
    working_time = sum([x.total_hours for x in courier.workdays])
    rating = orders_count / working_time * ratings_enum.get(courier.courier_type.value)
    courier.rating = rating
    courier.earnings = earnings

    return courier
