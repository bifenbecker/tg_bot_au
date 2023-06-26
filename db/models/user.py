import sqlalchemy as sa

from db.orm import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_id = sa.Column(sa.Integer)
    username = sa.Column(sa.String)
    telephone = sa.Column(sa.String)
    last_notify = sa.Column(sa.DateTime(timezone=True))
