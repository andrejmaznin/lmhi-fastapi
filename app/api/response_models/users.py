import enum


class GetSuccess(enum.Enum):
    success = "OK"
    users = {}

    def as_dict(self, users):
        return self.__dict__.update({"users": users})


class AuthSuccess(enum.Enum):
    success = "OK"

    def as_dict(self, sessions):
        return {self.success.name: self.success.value, "sessions": sessions}


class AuthLoginFailure(enum.Enum):
    message = "WRONG USERNAME, LOGIN, PHONE OR PASSWORD"


class AuthExitFailure(enum.Enum):
    user_id = "USER ID"
    session_id = "SESSION ID"

    def __init__(self, parameter):
        self.message = f"WRONG {parameter}"
