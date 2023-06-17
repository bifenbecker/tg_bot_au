import sqlalchemy as sa
from datetime import datetime
from db.orm import Base


class BflAnswer(Base):
    __tablename__ = "bfl_answers"

    id = sa.Column(sa.Integer, primary_key=True)
    chat_id = sa.Column(sa.Integer)
    region_name = sa.Column(sa.String)
    insolvent_situation = sa.Column(sa.String)
    amount_expense = sa.Column(sa.String)
    guarantees = sa.Column(sa.String)
    experience = sa.Column(sa.String)
    telephone = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           default=datetime.utcnow)
