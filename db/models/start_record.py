import sqlalchemy as sa
from datetime import datetime
from db.orm import Base


class StartRecord(Base):
    __tablename__ = "start_records"

    id = sa.Column(sa.Integer, primary_key=True)
    chat_id = sa.Column(sa.Integer)
    username = sa.Column(sa.String)
    start_time = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
