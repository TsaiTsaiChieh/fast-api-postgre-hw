from fastapi import APIRouter, HTTPException, status, Request
from app import settings

from db.schemas import User, LoginLog
from db.connection import session
from app.utils.verify import create_access_token, verify_token
from app.utils.login_utils import getUserInfoByAccount, createUserItem, createLoginLogs
from app.utils.schemas import UserRegisterSchema, UserRegisterOutSchema, UserLoginSchema, UserLoginOut

router = APIRouter(
    prefix=f'{settings.settings.api_prefix}/users', 
    tags=["users"]
)
    
# 新增使用者    
@router.post("/", response_model=UserRegisterOutSchema)
def postUser(user: UserRegisterSchema) -> UserRegisterOutSchema:
    query = getUserInfoByAccount(user.account)
    
    if query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="此帳號已被註冊")
    else:
        createUserItem(user)
        return UserRegisterOutSchema(**{
            "resp_code": status.HTTP_200_OK, 
            "resp_desc": "OK",
            "id": getUserInfoByAccount(user.account).id
        })

# 使用者登入驗證
@router.post("/login", response_model=UserLoginOut)
def userLogin(user: UserLoginSchema, request: Request) -> UserLoginOut:
    query = getUserInfoByAccount(user.account)
    if (not query.active): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="帳號被停用")
    
    if (query.password == user.password):
        createLoginLogs({"user_id": query.id, "login_ip": request.client.host})
        accessToken = create_access_token({
            "name": query.name,
            "account": query.account
        })
        
        return UserLoginOut(**{
            "resp_code": status.HTTP_200_OK, 
            "resp_desc": "OK",
            "token": accessToken, 
            "user":{
                "id": query.id,
                "account": query.account,
                "name": query.name,
                "active": query.active,
                "created_at": query.created_at,
                "updated_at": query.updated_at
            }})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="帳號密碼錯誤")
    
# @router.get("/users/test_token")
# def testToken():
    