from db.database import Base
from sqlalchemy import Column, Integer, String, Date

class Celebration(Base):
    __tablename__ = "celebrations"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    date = Column(Date,nullable=False)