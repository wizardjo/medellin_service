from db.database import Base
from sqlalchemy import Column, Integer, String

class Build(Base):
    __tablename__ = "buildings"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    cost = Column(Integer,nullable=False)
    preview_build = Column(String,nullable=False)
    experience_require = Column(Integer,nullable=False)