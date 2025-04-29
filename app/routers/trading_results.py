from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import TradeResult
from schemas import TradeResult as TradeResultSchema
from cache import cache_response

router = APIRouter(prefix="/trading_results", tags=["trading_results"])

@router.get("/", response_model=list[TradeResultSchema])
@cache_response
def get_trading_results(
    oil_id: Optional[str] = Query(None, description="Фильтр по oil_id"),
    delivery_type_id: Optional[str] = Query(None, description="Фильтр по delivery_type_id"),
    delivery_basis_id: Optional[str] = Query(None, description="Фильтр по delivery_basis_id"),
    db: Session = Depends(get_db)
):
    last_date = db.query(TradeResult.date).order_by(
        TradeResult.date.desc()
    ).first()
    
    if not last_date:
        return []
    
    query = db.query(TradeResult).filter(
        TradeResult.date == last_date[0]
    )
    
    if oil_id:
        query = query.filter(TradeResult.oil_id == oil_id)
    if delivery_type_id:
        query = query.filter(TradeResult.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.filter(TradeResult.delivery_basis_id == delivery_basis_id)
    
    return query.all()