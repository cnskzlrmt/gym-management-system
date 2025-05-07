# rate_limit.py
import time
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from auth import oauth2_scheme

# Global dictionary: token -> (window_start_time, request_count)
rate_limit_data = {}

RATE_LIMIT = 5          # Örneğin: 5 istek
RATE_LIMIT_WINDOW = 60  # 60 saniyelik pencere

async def rate_limiter(request: Request, token: str = Depends(oauth2_scheme)):
    current_time = time.time()
    if token not in rate_limit_data:
        rate_limit_data[token] = {"start": current_time, "count": 1}
    else:
        window = rate_limit_data[token]
        if current_time - window["start"] < RATE_LIMIT_WINDOW:
            if window["count"] >= RATE_LIMIT:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later."
                )
            else:
                window["count"] += 1
        else:
            rate_limit_data[token] = {"start": current_time, "count": 1}
