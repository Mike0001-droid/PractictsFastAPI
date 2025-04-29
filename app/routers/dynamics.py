from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from database import get_db
from models import TradeResult
from schemas import TradeResult as TradeResultSchema
from cache import cache_response


router = APIRouter(prefix="/dynamics", tags=["dynamics"])

@cache_response
@router.get("/", response_model=list[TradeResultSchema])
def get_dynamics(
    oil_id: Optional[str] = Query(None, description="Фильтр по oil_id"),
    delivery_type_id: Optional[str] = Query(None, description="Фильтр по delivery_type_id"),
    delivery_basis_id: Optional[str] = Query(None, description="Фильтр по delivery_basis_id"),
    start_date: datetime = Query(..., description="Начальная дата периода"),
    end_date: datetime = Query(..., description="Конечная дата периода"),
    db: Session = Depends(get_db)
):
    query = db.query(TradeResult).filter(
        TradeResult.date >= start_date,
        TradeResult.date <= end_date
    )
    
    if oil_id:
        query = query.filter(TradeResult.oil_id == oil_id)
    if delivery_type_id:
        query = query.filter(TradeResult.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.filter(TradeResult.delivery_basis_id == delivery_basis_id)
    result = query.order_by(TradeResult.id.desc()).limit(5)
    return result