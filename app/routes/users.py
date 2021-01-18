from fastapi import APIRouter, HTTPException, status
from app import settings

from db.schemas import User
from db.connection import session
from app.validators.postUser import PostUserIn, PostUserOut

router = APIRouter(
    prefix=settings.settings.api_prefix, 
    tags=["users"],
    responses={403: {"description": "已有相同帳號註冊"}}
)
    
    
@router.post("/users/", response_model=PostUserOut)
def postUser(user: PostUserIn) -> PostUserOut:
    query = session.query(User).filter(User.account == user.account).first()
    print(query)
    if query: 
        print('Found user')
        raise HTTPException(status_code=403, detail="已有相同帳號註冊")
    else:
        data = User(name=user.name, account=user.account, password=user.password, active=True)
        session.add(data)
        id = session.query(User.id).filter(User.name == user.name).first()
        session.commit()
        return {"resp_code": status.HTTP_200_OK, "resp_desc": "OK", "id": id[0]}
        # return PostUserOut(**{
        #     "resp_code": status.HTTP_200_OK, 
        #     "resp_desc": "OK",
        #     "id": id[0]
        # })