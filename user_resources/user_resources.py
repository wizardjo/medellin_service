from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db.database import Base


class UserResource(Base):
    __tablename__ = "user_resources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    food = Column(Integer, default=0)
    gold = Column(Integer, default=0)
    wood = Column(Integer, default=0)
    stone = Column(Integer, default=0)

    user = relationship("User", back_populates="resources")
