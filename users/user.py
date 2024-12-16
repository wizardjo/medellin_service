from db.database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    registerdatetime = Column(Date,nullable=False)
    disabled = Column(Boolean,nullable=False)