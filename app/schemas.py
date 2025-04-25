from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TradeResultBase(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str

    model_config = ConfigDict(from_attributes=True)


class TradeResultCreate(TradeResultBase):
    volume: float 
    total: float
    count: int
    date: datetime


class TradeResult(TradeResultCreate):
    id: int
    created_on: datetime
    updated_on: datetime

    model_config = ConfigDict(from_attributes=True)