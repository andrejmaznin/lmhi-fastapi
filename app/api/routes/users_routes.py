from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.response_models.users import *
from app.db import db_session
from app.db.db_models.users import User

router = APIRouter()


@router.get("/users", name="users", status_code=201, response_model=UserGetResponse, response_model_exclude_unset=True)
def get_user():
    session = db_session.create_session()

    users = session.query(User).all()
    users = [{"email": i.email, "hashed_password": i.hashed_password, "name": i.name, "info": i.info,
              "session": i.session} for i in users]

    response = Success.as_dict(Success, "users", users)
    return response


@router.post("/users", name="users", status_code=201, response_model=UserPostResponse,
             response_model_exclude_unset=True)
def post_user(user: UserIn):
    session = db_session.create_session()
    if not session.query(User).filter(User.email == user.email).all():
        user = User(
            name=user.name,
            hashed_password=user.hashed_password,
            email=user.email,
            info=user.info
        )
        session.add(user)
        session.commit()

        user_id = session.query(User).filter_by(
            email=user.email).one().id  # получаем id созданного пользователя, чтобы сообщить его в ответе

        return {"id": user_id, "success": "OK"}

    else:
        return JSONResponse(status_code=400, content={"ERROR": "USER ALREADY EXISTS"})
