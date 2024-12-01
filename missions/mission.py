from db.database import Base
from sqlalchemy import Column, Integer, String

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)