from fastapi import FastAPI
from database import engine, clear_cache_daily
from models import Base
from routers import trading_dates, dynamics, trading_results
import asyncio

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(trading_dates.router)
app.include_router(dynamics.router)
app.include_router(trading_results.router)

async def run_periodically():
    while True:
        if clear_cache_daily():
            print("Cache cleared at 14:11")
        await asyncio.sleep(60)  

# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(run_periodically())

@app.get("/")
def read_root():
    return {"message": "Spimex Trading API"}