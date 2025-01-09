from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from db.database import Base


class DailyLoginBonus(Base):
    __tablename__ = "daily_login_bonus"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    last_login_date = Column(Date, nullable=False)
    streak = Column(Integer, default=0)

    user = relationship("User", back_populates="daily_bonus")
