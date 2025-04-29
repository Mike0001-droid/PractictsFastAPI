from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import TradeResult
from cache import cache_response

router = APIRouter(prefix="/last_trading_dates", tags=["trading_dates"])


@cache_response
@router.get("/", response_model=list[datetime])
def get_last_trading_dates(
    limit: int = Query(10, description="Количество последних торговых дней"),
    db: Session = Depends(get_db)
):
    dates = db.query(TradeResult.date).distinct().order_by(
        TradeResult.date.desc()
    ).limit(limit).all()
    return [date[0] for date in dates]