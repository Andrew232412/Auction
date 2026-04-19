import time
from typing import Optional, Dict
from jose import JWTError, jwt
from ..config import settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # python-jose expects numeric "exp" (Unix seconds), not datetime
    exp = int(time.time()) + settings.access_token_expire_minutes * 60
    to_encode.update({"exp": exp, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    exp = int(time.time()) + settings.refresh_token_expire_days * 24 * 60 * 60
    to_encode.update({"exp": exp, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> Optional[Dict]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None
