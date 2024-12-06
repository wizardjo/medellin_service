from db.database import Base
from sqlalchemy import Column, Integer, String

class Buid(Base):
    __tablename__ = "builds"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    cost = Column(Integer,nullable=False)
    previewBuild = Column(String,nullable=False)
    experienceRequire = Column(Integer,nullable=False)