from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from app import crud, models, schemas
from app.db import SessionLocal, engine
from app import services

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address, default_limits=["10/second"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/couriers/",
    response_model=schemas.CreateCouriersResponse,
    tags=["courier"],
)
def create_couriers(
    couriers: list[schemas.CreateCourierDto], db: Session = Depends(get_db)
):
    created = crud.create_couriers(db=db, couriers=couriers)
    return schemas.CreateCouriersResponse.parse_obj({"couriers": created})


@app.get("/couriers/{courier_id}", response_model=schemas.CourierDto, tags=["courier"])
def get_courier(courier_id: int, db: Session = Depends(get_db)):
    obj = crud.get_courier(db=db, courier_id=courier_id)
    if not obj:
        raise HTTPException(status_code=404)
    return crud.get_courier(db=db, courier_id=courier_id)


@app.get("/couriers/", response_model=schemas.GetCouriersResponse, tags=["courier"])
def get_couriers(limit: int = 1, offset: int = 0, db: Session = Depends(get_db)):
    objs = crud.get_couriers(db=db, limit=limit, offset=offset)
    return schemas.GetCouriersResponse.parse_obj(
        {"limit": limit, "offset": offset, "couriers": objs}
    )


@app.get(
    "/couriers/meta-info/{courier_id}",
    response_model=schemas.GetCourierMetaInfoResponse,
    tags=["courier"],
)
async def get_courier_meta_info(
    courier_id: int, start_date: str, end_date: str, db: Session = Depends(get_db)
):
    obj = services.get_courier_meta_info(db, courier_id, start_date, end_date)
    return obj


@app.post("/orders", response_model=list[schemas.OrderDto], tags=["order"])
async def create_orders(
    orders: list[schemas.CreateOrderDto], db: Session = Depends(get_db)
):
    created_orders = crud.create_orders(db=db, orders=orders)
    return created_orders


@app.get("/orders", response_model=list[schemas.OrderDto], tags=["order"])
async def get_orders(limit: int = 1, offset: int = 0, db: Session = Depends(get_db)):
    return crud.get_orders(db, limit, offset)


@app.get("/orders/{order_id}", response_model=schemas.OrderDto, tags=["order"])
async def get_order(order_id: int, db: Session = Depends(get_db)):
    obj = crud.get_order(db=db, order_id=order_id)
    if not obj:
        raise HTTPException(status_code=404)
    return obj


@app.post("/orders/complete", response_model=list[schemas.OrderDto], tags=["order"])
async def complete_order(
    complete_info: schemas.CompleteOrderRequestDto, db: Session = Depends(get_db)
):
    objs = services.complete_order(db, complete_info.complete_info)
    if not objs:
        raise HTTPException(status_code=404)
    return objs
