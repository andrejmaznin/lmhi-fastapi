from fastapi import APIRouter

from app.api.response_models.users import AuthSuccess, GetSuccess
from app.db import db_session
from app.db.db_models.users import User

router = APIRouter()


@router.get("/users", name="users", status_code=201)
def get_user():
    session = db_session.create_session()

    users = session.query(User).all()
    users = [{"email": i.email, "hashed_password": i.hashed_password, "name": i.name, "info": i.info,
              "session": i.session} for i in users]

    response = GetSuccess.as_dict(GetSuccess, users)
    return response


@router.post("/users", name="users", status_code=201)
def post_user(self):
    payload = request.get_json(force=True)

    session = db_session.create_session()
    if not session.query(User).filter(User.email == payload["email"]).all():
        user = User(
            name=payload['name'],
            hashed_password=payload["hashed_password"],
            email=payload['email'],
            info=payload['info']
        )
        session.add(user)
        user_id = session.query(User).filter_by(
            email=payload["email"]).one().id  # получаем id созданного пользователя, чтобы сообщить его в ответе
        session.commit()
        response = jsonify({'success': 'OK', "id": user_id})
        response.status_code = 201
        return response
    else:
        response = jsonify({'ERROR': 'USER ALREADY EXISTS'})
        response.status_code = 400
        return response