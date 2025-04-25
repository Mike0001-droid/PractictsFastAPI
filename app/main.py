from fastapi import FastAPI
from database import engine
from models import Base
from routers import trading_dates, dynamics, trading_results

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(trading_dates.router)
app.include_router(dynamics.router)
app.include_router(trading_results.router)

@app.get("/")
def read_root():
    return {"message": "Spimex Trading API"}