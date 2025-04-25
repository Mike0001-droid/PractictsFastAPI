from functools import wraps
from datetime import datetime, timedelta
from fastapi import HTTPException
import json
from database import redis_client

def cache_response(expire_minutes=60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from .database import clear_cache_daily
            clear_cache_daily()
            
            cache_key = f"{func.__name__}:{str(kwargs)}"
            
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
            redis_client.setex(
                cache_key,
                timedelta(minutes=expire_minutes),
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator