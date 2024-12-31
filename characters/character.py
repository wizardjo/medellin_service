from db.database import Base
from sqlalchemy import Column, Integer, String

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)