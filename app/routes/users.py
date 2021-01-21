# Standard
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from fastapi_jwt_auth.exceptions import AuthJWTException

# Project
from app import settings
from db.schemas import User, LoginLog
from db.connection import session
from app.utils.verify import createAccessToken, verifyToken
from app.utils.login_utils import getUserInfoByAccount, createUserItem, createLoginLogs
from app.utils.schemas import (
    ResultResponse,
    UserRegisterSchema,
    UserRegisterOutSchema,
    UserLoginSchema,
    UserLoginOut,
)


router = APIRouter(prefix=f"{settings.settings.api_prefix}/users", tags=["users"])


@AuthJWT.load_config
def get_config():
    return settings.settings


denylist = set()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in denylist


# 新增使用者
@router.post("/", response_model=UserRegisterOutSchema)
def postUser(user: UserRegisterSchema) -> UserRegisterOutSchema:
    query = getUserInfoByAccount(user.account)

    if query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="此帳號已被註冊")
    else:
        createUserItem(user)
        return UserRegisterOutSchema(
            **{
                "resp_code": status.HTTP_200_OK,
                "resp_desc": "OK",
                "id": getUserInfoByAccount(user.account).id,
            }
        )


# 使用者登入驗證
@router.post("/login", response_model=UserLoginOut)
def userLogin(
    user: UserLoginSchema, request: Request, Authorize: AuthJWT = Depends()
) -> UserLoginOut:
    query = getUserInfoByAccount(user.account)
    if not query.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="帳號被停用")

    if query.password == user.password:
        createLoginLogs({"user_id": query.id, "login_ip": request.client.host})
        accessToken = createAccessToken(
            {"name": query.name, "account": query.account}, Authorize
        )

        return UserLoginOut(
            **{
                "resp_code": status.HTTP_200_OK,
                "resp_desc": "OK",
                "token": accessToken,
                "user": {
                    "id": query.id,
                    "account": query.account,
                    "name": query.name,
                    "active": query.active,
                    "created_at": query.created_at,
                    "updated_at": query.updated_at,
                },
            }
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="帳號密碼錯誤")


@router.delete("/login")
def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()["jti"]
        denylist.add(jti)
    except AuthJWTException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token or access token expired",
        )

    return ResultResponse(**{"resp_code": status.HTTP_200_OK, "resp_desc": "OK"})


@router.get("/current_user")
def currentUser(Authorize: AuthJWT = Depends()):
    return verifyToken(Authorize)
