import sqlalchemy
from sqlalchemy import orm
from app.db.db_session import SqlAlchemyBase


class HabitName(SqlAlchemyBase):
    __tablename__ = 'habit_names'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
