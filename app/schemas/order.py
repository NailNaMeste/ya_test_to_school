import datetime

from pydantic import BaseModel, validator, Field
from app.models import CourierType
from app.utils import str_hours_to_datetime


#
# def str_to_datetime(time: str):
#     hour =
#     now = datetime.datetime.now().replace(hour=)
#     return datetime.datetime.strptime()


class BaseOrderDto(BaseModel):
    weight: float
    regions: list[int]
    delivery_hours: list[str]
    cost: int
    _delivery_hours_start: list[datetime] = Field()
    _delivery_hours_end: list[datetime] = Field()

    class Config:
        orm_mode = True

    @validator("delivery_hours")
    def get_delivery_hours(cls, value):
        cls._delivery_hours_start, cls._delivery_hours_end = str_hours_to_datetime(
            value
        )
        return value


class CreateOrderDto(BaseOrderDto):
    pass


class OrderDto(BaseOrderDto):
    complete_time: datetime.datetime | None
    order_id: int


class CompleteOrderDto(BaseModel):
    complete_time: datetime.datetime | None
    courier_id: int
    order_id: int


class CompleteOrderRequestDto(BaseModel):
    complete_info: list[CompleteOrderDto]
