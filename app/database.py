from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from sqlalchemy.orm import sessionmaker
import redis
from datetime import datetime, time


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
REDIS_URL = "redis://localhost:6379"
redis_client = redis.Redis.from_url(REDIS_URL)

def clear_cache_daily():
    now = datetime.now().time()
    target_time = time(14, 11)
    
    if now.hour == target_time.hour and now.minute == target_time.minute:
        redis_client.flushdb()
        return True
    return False


class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()