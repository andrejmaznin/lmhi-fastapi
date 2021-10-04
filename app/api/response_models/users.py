from pydantic import BaseModel


class UserPostIn(BaseModel):
    name: str
    hashed_password: str
    email: str
    info: str


class SessionsGetResponse(BaseModel):
    success: bool
    sessions: list


class UserExitIn(BaseModel):
    success: bool
    id: int
    login: str


class UserExitOut(BaseModel):
    success: bool


class UserLoggedIn(BaseModel):
    session_id: int
    success = bool


class UserAuthIn(BaseModel):
    login: str
    hashed_password: str


class UserGetResponse(BaseModel):
    success = bool
    users: list


class UserOut(BaseModel):
    id: int
    success = bool
