import sqlalchemy
import sqlalchemy.exc
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import or_

from app.api.response_models.users import *
from app.db import db_session
from app.db.db_models.auth_sessions import Session
from app.db.db_models.users import User

router = APIRouter()


@router.get("/users", name="users", status_code=201, response_model=UserGetResponse, response_model_exclude_unset=True)
def get_user():
    session = db_session.create_session()

    users = session.query(User).all()
    users = [{"email": i.email, "hashed_password": i.hashed_password, "name": i.name, "info": i.info,
              "session": i.session} for i in users]
    return {"success": True, "users": users}


@router.post("/users", name="users", status_code=201, response_model=UserOut,
             response_model_exclude_unset=True)
def post_user(user: UserPostIn):
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

        return {"id": user_id, "success": True}

    else:
        return JSONResponse(status_code=400, content={"ERROR": "USER ALREADY EXISTS"})


@router.post("/auth/login", name="login", status_code=201, response_model=UserLoggedIn,
             response_model_exclude_unset=True)
def post_auth_login(user_in: UserAuthIn):
    session = db_session.create_session()

    try:
        user = session.query(User).filter(
            or_(User.email == user_in.login, User.phone == user_in.login,
                User.login == user_in.login)).one()

    except sqlalchemy.exc.NoResultFound:
        return JSONResponse(status_code=400, content={'ERROR': 'NO USER'})

    if user_in.hashed_password == user.hashed_password:
        auth = Session(
            user_id=user.id)

        session.add(auth)
        session.commit()

        session_id = session.query(Session).filter_by(user_id=user.id).all()[-1].id
        user.session = user.session + [session_id] if user.session else [session_id]

        session.commit()
        return {"session_id": session_id, 'success': True}

    return JSONResponse(status_code=400, content={"ERROR": "WRONG USERNAME, LOGIN, PHONE OR PASSWORD"})


@router.post("/auth/exit", name="exit", status_code=201, response_model=UserExited,
             response_model_exclude_unset=True)
def post_auth_exit(user_in: UserExitIn):
    session = db_session.create_session()

    try:
        user = session.query(User).filter(
            or_(User.email == user_in.login, User.phone == user_in.login,
                User.login == user_in.login)).one()

    except sqlalchemy.exc.NoResultFound:
        return JSONResponse(status_code=400, content={'ERROR': 'NO USER'})

    auth_session = session.query(Session).get(user_in.id)
    if auth_session.id:
        if auth_session.user_id == user.id:
            session.query(Session).filter_by(id=user.id).delete()
            session.commit()

            return {'success': True}

        return JSONResponse(status_code=400, content={'ERROR': 'WRONG USER ID'})

    return JSONResponse(status_code=400, content={'ERROR': 'WRONG SESSION ID'})


@router.get("/auth", name="auth", status_code=201, response_model=SessionsGetResponse,
            response_model_exclude_unset=True)
def session_get():
    session = db_session.create_session()

    sessions = session.query(Session).all()
    sessions = [{"id": i.id, "user_id": i.user_id} for i in
                sessions]
    return {"sessions": sessions, "success": True}
