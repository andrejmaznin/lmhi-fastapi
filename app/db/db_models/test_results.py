import sqlalchemy
from sqlalchemy import orm
from app.db.db_session import SqlAlchemyBase


class Test_result(SqlAlchemyBase):
    __tablename__ = 'test_results'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    result = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
