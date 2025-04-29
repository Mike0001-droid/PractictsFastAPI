from httpx import AsyncClient, ASGITransport
import pytest
from app.main import app as FastaAPIApp
from app.schemas import TradeResult


@pytest.mark.asyncio
async def test_last_trading_dates():
    async with AsyncClient(
            transport=ASGITransport
            (FastaAPIApp),
            base_url="http://test",
        ) as ac:
        response = await ac.get("/last_trading_dates/")
        data = response.json()
        assert len(data) == 10


@pytest.mark.asyncio
async def test_get_dynamics():
    async with AsyncClient(
            transport=ASGITransport
            (FastaAPIApp),
            base_url="http://test",
        ) as ac:
        response = await ac.get("/dynamics/", params={
            "start_date": '2025-04-11T00:00:00',
            "end_date": '2025-04-11T00:00:00'
            }
        )
        trade_results = response.json()
        for trade_result in trade_results:
            assert TradeResult.model_validate(trade_result)
