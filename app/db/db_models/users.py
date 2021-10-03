import sqlalchemy

from app.db.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    session = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer), nullable=True)
