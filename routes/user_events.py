from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from db.database import engine
from schemas.schemas import (
    UserEventResponse,
    UserEventBase,
)

router = APIRouter()


@router.post(
    "/user-events/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserEventResponse,
    tags=["User Events"],
)
def create_user_event(event: UserEventBase):
    #  Consulta SQL segura con parámetros
    query = text(
        "INSERT INTO user_events (user_id, event_name, timestamp) VALUES (:user_id, :event_name, :timestamp) RETURNING id"
    )
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(
                query,
                {
                    "user_id": event.user_id,
                    "event_name": event.event_name,
                    "timestamp": event.timestamp,
                },
            )

            # Obtenemos el ID generado por la base de datos
            event_id = result.scalar()
            con.commit()

            # Devolvemos el nuevo objeto de evento con el ID asignado
            new_event = UserEventResponse(
                id=event_id,
                user_id=event.user_id,
                event_name=event.event_name,
                timestamp=event.timestamp,
            )
            return new_event

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating the event: {str(e)}",
            )
