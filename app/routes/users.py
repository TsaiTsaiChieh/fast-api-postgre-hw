from fastapi import APIRouter, HTTPException, status, Request
from app import settings

from db.schemas import User, LoginLog
from db.connection import session
from app.validators.postUser import PostUserIn, PostUserOut
from app.utils.verify import create_access_token, verify_token
from app.validators.userLogin import UserLoginIn, UserLoginOut

router = APIRouter(
    prefix=settings.settings.api_prefix, 
    tags=["users"],
    responses={403: {"description": "已有相同帳號註冊"}}
)
    
# 新增使用者    
@router.post("/users/", response_model=PostUserOut)
def postUser(user: PostUserIn) -> PostUserOut:
    query = session.query(User).filter(User.account == user.account).first()
    
    if query: 
        print('Found user')
        raise HTTPException(status_code=403, detail="已有相同帳號註冊")
    else:
        data = User(name=user.name, account=user.account, password=user.password, active=True)
        session.add(data)
        id = session.query(User.id).filter(User.name == user.name).first()[0]
        session.commit()
        return {"resp_code": status.HTTP_200_OK, "resp_desc": "OK", "id": id}
        # return PostUserOut(**{
        #     "resp_code": status.HTTP_200_OK, 
        #     "resp_desc": "OK",
        #     "id": id[0]
        # })

# 使用者登入驗證
@router.post("/users/login", response_model=UserLoginOut)
def userLogin(user: UserLoginIn, request: Request) -> UserLoginOut:
    print(request.client)
    userInfo = session.query(User).filter(User.account == user.account).first()
    if (not userInfo.active): 
        raise HTTPException(status_code=403, detail="帳號被停用")
    
    if (userInfo.password == user.password):
        data = LoginLog(user_id=userInfo.id, login_ip=request.client.host)
        session.add(data)
        session.commit()
        accessToken = create_access_token({
            "name": userInfo.name,
            "account": userInfo.account
        })
        
        return UserLoginOut(
            **{"resp_code": status.HTTP_200_OK, 
               "resp_desc": "OK",
               "token": accessToken, 
               "user":{
                   "id": userInfo.id,
                   "account": userInfo.account,
                   "name": userInfo.name,
                   "active": userInfo.active,
                   "created_at": userInfo.created_at,
                   "updated_at": userInfo.updated_at
                      }
               }
            )
    else:
        raise HTTPException(status_code=401, detail="帳號密碼錯誤")