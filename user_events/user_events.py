from db.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.orm import relationship
from datetime import datetime


class UserEvent(Base):
    __tablename__ = "user_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_name = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)

  # Relación inversa hacia el modelo User
    user = relationship("User", back_populates="events")