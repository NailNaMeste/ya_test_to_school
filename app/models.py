import datetime
import enum

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    ARRAY,
    Enum,
    Float,
    DateTime,
    Date,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db import Base
from app.utils import str_to_datetime


class CourierType(enum.Enum):
    foot = "FOOT"
    cycle = "BIKE"
    car = "AUTO"


class Courier(Base):
    __tablename__ = "couriers"

    courier_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    courier_type = Column(Enum(CourierType))
    regions = Column(ARRAY(Integer))  # move to CourierWorkDay?
    orders = relationship("Order", back_populates="courier", lazy="dynamic")
    working_hours = Column(ARRAY(String))
    workdays = relationship("CourierWorkDay", back_populates="courier", lazy="dynamic")


class CourierWorkDay(Base):
    __tablename__ = "workdays"

    courier_id = Column(Integer, ForeignKey("couriers.courier_id"))
    courier = relationship("Courier", back_populates="workdays")

    workday_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, default=datetime.date.today)

    working_hours = Column(ARRAY(String))

    @hybrid_property
    def working_hours_to_datetime(
        self,
    ) -> list[tuple[datetime.datetime, datetime.datetime]]:
        result = []
        for item in self.working_hours:
            result.append(str_to_datetime(item))
        return result

    @hybrid_property
    def total_hours(self):
        total = 0
        for start, end in self.working_hours_to_datetime:
            print(start, end)
            total += round((end - start).total_seconds() / 60 / 60, 2)
        return total


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    weight = Column(Float)
    regions = Column(ARRAY(Integer))

    cost = Column(Integer)
    complete_time = Column(DateTime, nullable=True)

    delivery_hours = Column(ARRAY(String))
    # delivery_hours_start = Column(ARRAY(DateTime), )
    # delivery_hours_end = Column(ARRAY(DateTime))

    courier_id = Column(Integer, ForeignKey("couriers.courier_id"), nullable=True)
    courier = relationship("Courier", back_populates="orders")
