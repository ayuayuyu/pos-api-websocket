from pydantic import BaseModel


class Datas(BaseModel):
    state: str
    key: str