from db.database import Base
from sqlalchemy import Column, Integer, String

class Build(Base):
    __tablename__ = "buildings"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    cost = Column(Integer,nullable=False)
    previewbuild = Column(String,nullable=False)
    experiencerequire = Column(Integer,nullable=False)