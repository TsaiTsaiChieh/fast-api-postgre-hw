# Standard
# Project
from db.connection import session
from db.schemas import User, LoginLog
from utils.schemas import UserRegisterSchema, LoginLogSchema


def getUserInfoByAccount(account: str):
    return session.query(User).filter(User.account == account).first()


def createUserItem(user: UserRegisterSchema):
    data = User(
        name=user.name, account=user.account, password=user.password, active=True
    )
    session.add(data)
    session.commit()


def createLoginLogs(loginLog: LoginLogSchema):
    data = LoginLog(user_id=loginLog["user_id"], login_ip=loginLog["login_ip"])
    session.add(data)
    session.commit()