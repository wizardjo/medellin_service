from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from db.database import engine
from schemas.schemas import DailyBonusResponse
from datetime import date, timedelta

router = APIRouter()

@router.post(
    "/daily-login-bonus/",
    status_code=status.HTTP_200_OK,
    response_model=DailyBonusResponse,
    tags=["Daily Login Bonus"],
)
def daily_login_bonus(user_id: int):
    today = date.today()

    # Query para verificar si el usuario tiene un registro de daily_login_bonus
    select_query = text(
        """
        SELECT id, user_id, last_login_date, streak
        FROM daily_login_bonus
        WHERE user_id = :user_id
        """
    )

    # Query para insertar un nuevo registro
    insert_query = text(
        """
        INSERT INTO daily_login_bonus (user_id, last_login_date, streak)
        VALUES (:user_id, :last_login_date, :streak)
        RETURNING id, user_id, last_login_date, streak
        """
    )

    # Query para actualizar el registro existente
    update_query = text(
        """
        UPDATE daily_login_bonus
        SET last_login_date = :last_login_date,
            streak = :streak
        WHERE user_id = :user_id
        RETURNING id, user_id, last_login_date, streak
        """
    )

    # Query para actualizar los recursos del usuario
    update_resources_query = text(
        """
        UPDATE user_resources
        SET food = food + :food,
            gold = gold + :gold,
            wood = wood + :wood,
            stone = stone + :stone
        WHERE user_id = :user_id
        """
    )

    with engine.connect() as con:
        try:
            # Verificar si el usuario tiene un registro en daily_login_bonus
            result = con.execute(select_query, {"user_id": user_id}).fetchone()

            if not result:
                # Crear un nuevo registro si no existe
                new_bonus = con.execute(
                    insert_query,
                    {
                        "user_id": user_id,
                        "last_login_date": today,
                        "streak": 1,
                    },
                ).fetchone()
                con.commit()

                # Aplicar el bono inicial
                bonus = {"food": 50, "gold": 20, "wood": 30, "stone": 10}
                con.execute(
                    update_resources_query,
                    {
                        "user_id": user_id,
                        **bonus,
                    },
                )
                con.commit()

                return DailyBonusResponse(
                    message="Welcome! Here is your first daily bonus.",
                    bonus=bonus,
                    streak=new_bonus.streak,
                )

            # Si ya reclamó el bono hoy, devolver un error
            last_login_date = result.last_login_date
            if last_login_date == today:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Daily bonus already claimed.",
                )

            # Calcular la racha
            streak = result.streak
            if last_login_date == today - timedelta(days=1):
                streak += 1
            else:
                streak = 1

            # Actualizar el registro
            updated_bonus = con.execute(
                update_query,
                {
                    "user_id": user_id,
                    "last_login_date": today,
                    "streak": streak,
                },
            ).fetchone()
            con.commit()

            # Calcular el bono basado en la racha
            bonus = calculate_bonus(streak)

            # Aplicar el bono
            con.execute(
                update_resources_query,
                {
                    "user_id": user_id,
                    **bonus,
                },
            )
            con.commit()

            return DailyBonusResponse(
                message="Daily bonus claimed!",
                bonus=bonus,
                streak=updated_bonus.streak,
            )
        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while processing the daily login bonus: {str(e)}",
            )


def calculate_bonus(streak: int):
    """Calcula el bono basado en la racha."""
    if streak == 1:
        return {"food": 50, "gold": 20, "wood": 30, "stone": 10}
    elif streak == 7:
        return {"food": 100, "gold": 50, "wood": 50, "stone": 20}
    else:
        return {
            "food": 10 * streak,
            "gold": 5 * streak,
            "wood": 5 * streak,
            "stone": 2 * streak,
        }
