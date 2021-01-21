# Standard
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

# Project
from app import settings


def createAccessToken(
    data: dict,
    Authorize: AuthJWT = Depends(),
    expiredDelta: Optional[int] = None,
) -> str:
    if expiredDelta:
        expire = timedelta(expiredDelta)
    else:
        expire = timedelta(minutes=settings.settings.access_token_expired_minutes)
    encodeJWT = Authorize.create_access_token(subject=str(data), expires_time=expire)
    return encodeJWT


def verifyToken(Authorize: AuthJWT = Depends()):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing token or access token expired",
    )
    try:
        Authorize.jwt_required()
        payload = Authorize.get_jwt_subject()
    except AuthJWTException:
        raise credentialsException
    return eval(payload)
