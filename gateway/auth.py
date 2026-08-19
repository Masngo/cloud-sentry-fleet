import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("GATEWAY_API_KEY", "dev-secret-key"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key
