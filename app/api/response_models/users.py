from enum import Enum

from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    hashed_password: str
    email: str
    info: str


class Success(Enum):
    success = "OK"

    def as_dict(self, name: str, payload: list):
        response = {self.success.name: self.success.value, name: payload}
        return response


class Failure(Enum):
    id = "USER ID"
    session = "SESSION"
    login = "USERNAME, LOGIN OR PASSWORD"

    def as_dict(self, payload):
        value = eval(f"self.{payload}")
        return self.dict().update({"ERROR": f"WRONG {value}"})


class UserGetResponse(BaseModel):
    success = "OK"
    users: list


class UserPostResponse(BaseModel):
    id: int
    success = "OK"
