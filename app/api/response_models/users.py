from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    hashed_password: str
    email: str
    info: str


class UserLoggedIn(BaseModel):
    session_id: int
    success = bool


class UserAuthIn(BaseModel):
    login: str
    hashed_password: str


class UserGetResponse(BaseModel):
    success = bool
    users: list


class UserPostResponse(BaseModel):
    id: int
    success = bool
