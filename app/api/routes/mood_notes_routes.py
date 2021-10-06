from fastapi import APIRouter
from app.db.db_models.mood_notes import MoodNote
from app.api.request_models.users import *

router = APIRouter()


@router.get("/mood_notes", name="mood_notes", status_code=201, response_model=UserGetResponse,
            response_model_exclude_unset=True)
def get():  # получение всех записей по user_id и scale_id. Требуется session_id, user_id, scale_id
    payload = request.get_json()
    session = db_session.create_session()
    try:
        if check_session(payload['session_id'],
                         payload['user_id']):  # проверка наличия пользователя с такой сессией

            # возвращение списка дневника настроений по пользователю и настроению
            mood_notes = [note.as_dict() for note in
                          session.query(MoodNote).filter(MoodNote.user_id == payload['user_id'],
                                                         MoodNote.scale_id == payload['scale_id']).all()]
            response = jsonify({'success': 'OK', "mood_notes": mood_notes})
            response.status_code = 201
            return response
        else:
            response = jsonify({'ERROR': "NO USER WITH THE SESSION"})
            response.status_code = 400
            return response

    except Exception as error:
        response = jsonify({"ERROR": traceback.format_exc(error)})
        response.status_code = 400
        return response
