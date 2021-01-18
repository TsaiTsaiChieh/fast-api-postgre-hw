from pydantic import BaseModel

class ResultResponse(BaseModel):
    resp_code: int
    resp_desc: str