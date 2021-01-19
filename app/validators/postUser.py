from pydantic import BaseModel, constr, ValidationError, validator
from app.validators.resultResponse import ResultResponse


class PostUserIn(BaseModel):
    account: constr(min_length=4, max_length=12)
    password: constr(min_length=8, max_length=12)
    password_confirm: constr(min_length=8, max_length=12)
    name: constr(max_length=10)
    
    @validator("password_confirm")
    # cls = <class 'routes.users.PostUser'>
    # v = values["password_confirm"]
    # values = request.body
    def passwordsMatch(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v
    
class PostUserOut(ResultResponse):
    id: int
    
class UserLoginIn(BaseModel):
    account: constr(min_length=4, max_length=12)
    password: constr(min_length=8, max_length=12)