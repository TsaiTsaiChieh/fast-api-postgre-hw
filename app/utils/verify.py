from app import settings
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError

SECRET_KEY = settings.settings.secret_key
ALGORITHM = settings.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.settings.access_token_expired_minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
    
def verify_token(token: str):
    try:
        return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except (JWTError, ExpiredSignatureError):
        raise e