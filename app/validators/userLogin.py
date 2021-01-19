from pydantic import BaseModel, constr, ValidationError, validator
from app.validators.resultResponse import ResultResponse
from datetime import datetime
    
class User(BaseModel):
    id: int
    account: constr(min_length=4, max_length=12)
    active: bool
    created_at: datetime
    updated_at: datetime
    
class UserLoginIn(BaseModel):
    account: constr(min_length=4, max_length=12)
    password: constr(min_length=8, max_length=12)

class UserLoginOut(ResultResponse):
    token: str
    user: User
