from pydantic import BaseModel, constr, validator, EmailStr
from ipaddress import IPv4Address
from fastapi import HTTPException, status
import re
from typing import List, Optional, Dict
from datetime import datetime

class ResultResponse(BaseModel):
    resp_code: int
    resp_desc: str
    
class UserRegisterSchema(BaseModel):
    name: constr(max_length=10)
    account: EmailStr
    password: constr(min_length=6, max_length=16)
    password_confirm: constr(min_length=6, max_length=16)

    # 驗證密碼只能包含數字或英文
    @validator("password")
    def passwordAlphanumeric(cls, v):
        if not re.match("^[A-Za-z0-9_-]*$", v):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password should only contain either alphabets or numbers")
        return v

    # 驗證第二次密碼有無一致
    @validator("password_confirm")
    # cls = <class 'router.users.UserRegisterSchema'>
    # v = values["password_confirm"]
    # values = request.body
    def passwordsMatch(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Passwords do not match")
        return v

class UserRegisterOutSchema(ResultResponse):
    id: int

class User(BaseModel):
    id: int
    account: EmailStr
    active: bool
    created_at: datetime
    updated_at: datetime
    
class UserLoginSchema(BaseModel):
    account: EmailStr
    password: constr(min_length=8, max_length=12)

class UserLoginOut(ResultResponse):
    token: str
    user: User
    
class LoginLogSchema(BaseModel):
    user_id: int
    login_ip: IPv4Address