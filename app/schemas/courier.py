from pydantic import BaseModel, Extra

from app.models import CourierType


class BaseCourierDto(BaseModel):
    courier_type: CourierType
    regions: list[int] = []
    working_hours: list[str] = []

    class Config:
        orm_mode = True
        extra = Extra.allow


class CourierDto(BaseCourierDto):
    courier_id: int


class CreateCourierDto(BaseCourierDto):
    pass


class CreateCouriersResponse(BaseModel):
    couriers: list[CourierDto]

    class Config:
        orm_mode = True


class GetCouriersResponse(BaseModel):
    couriers: list[CourierDto]
    limit: int
    offset: int


class GetCourierMetaInfoResponse(CourierDto):
    rating: int = None
    earnings: int = None
