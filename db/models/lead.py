import sqlalchemy as sa
from datetime import datetime
from db.orm import Base


class LeadAnswer(Base):
    __tablename__ = "lead_answers"

    id = sa.Column(sa.Integer, primary_key=True)
    chat_id = sa.Column(sa.Integer)
    region_name = sa.Column(sa.String)
    business_info = sa.Column(sa.String)
    amount_clients = sa.Column(sa.String)
    telephone = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           default=datetime.utcnow)
