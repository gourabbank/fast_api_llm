
import time
from fastapi import HTTPException

user_requests = {}
GLOBAL_RATE_LIMIT = 3  # Max requests per time window
GLOBAL_TIME_WINDOW_SECONDS = 60  # Time window in seconds

def apply_rate_limiting(ip_address: str) -> bool:
    # Implement rate limiting logic here
    # For example, you can use an in-memory store or a database to track request counts
    # Return True if the request is allowed, False if it should be blocked

    current_time = time.time()
    rate_limit_window = GLOBAL_RATE_LIMIT  # Time window in seconds
    time_window=GLOBAL_TIME_WINDOW_SECONDS

    if ip_address not in user_requests:
        user_requests[ip_address] = []

    user_requests[ip_address]=[
        t for t in user_requests[ip_address] if t>=current_time - time_window
    ]

    if len(user_requests[ip_address]) >= rate_limit_window:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    
    user_requests[ip_address].append(current_time)
    return True  # Placeholder implementation