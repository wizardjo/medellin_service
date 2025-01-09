from db.database import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    registerdatetime = Column(String, nullable=False)

    # Relación con eventos (uno-a-muchos)
    # Propósito: Rastrear todos los eventos generados por el usuario (como clics, acciones, etc.).
    events = relationship(
        "UserEvent", back_populates="user", cascade="all, delete-orphan"
    )

    # Relación con recursos (uno-a-uno)
    # Propósito: Almacenar el estado actual de los recursos del usuario (food, gold, wood, stone)
    resources = relationship(
        "UserResource",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Relación con bono diario (uno-a-uno)
    # Propósito: Almacenar la última fecha de inicio de sesión y la racha diaria del usuario
    daily_bonus = relationship(
        "DailyLoginBonus",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
