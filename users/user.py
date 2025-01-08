from db.database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(String,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    registerdatetime = Column(String,nullable=False)