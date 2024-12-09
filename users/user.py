from db.database import Base
from sqlalchemy import Column, Integer, String, Date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    surname = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    registerDateTime = Column(Date,nullable=False )