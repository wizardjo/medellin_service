from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from db.database import engine
from schemas.schemas import (
    UserResourceResponse,
    UserResourceBase,
    UserResourceUpdate,
)

router = APIRouter()


# Crear o inicializar recursos para un usuario
@router.post(
    "/resources/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResourceResponse,
    tags=["Resources"],
)
def create_user_resources(resource: UserResourceBase):
    query = text(
        """
        INSERT INTO user_resources (user_id, food, gold, wood, stone)
        VALUES (:user_id, :food, :gold, :wood, :stone)
        RETURNING id
        """
    )
    with engine.connect() as con:
        try:
            result = con.execute(
                query,
                {
                    "user_id": resource.user_id,
                    "food": resource.food,
                    "gold": resource.gold,
                    "wood": resource.wood,
                    "stone": resource.stone,
                },
            )
            resource_id = result.scalar()
            con.commit()

            return UserResourceResponse(
                id=resource_id,
                user_id=resource.user_id,
                food=resource.food,
                gold=resource.gold,
                wood=resource.wood,
                stone=resource.stone,
            )
        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating resources: {str(e)}",
            )


# Actualizar recursos existentes para un usuario
@router.put(
    "/resources/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResourceResponse,
    tags=["Resources"],
)
def update_user_resources(user_id: int, update: UserResourceUpdate):
    select_query = text(
        """
        SELECT id, user_id, food, gold, wood, stone
        FROM user_resources
        WHERE user_id = :user_id
        """
    )
    update_query = text(
        """
        UPDATE user_resources
        SET food = food + :food,
            gold = gold + :gold,
            wood = wood + :wood,
            stone = stone + :stone
        WHERE user_id = :user_id
        RETURNING id, user_id, food, gold, wood, stone
        """
    )
    with engine.connect() as con:
        try:
            # Verificar si el usuario tiene recursos inicializados
            result = con.execute(select_query, {"user_id": user_id}).fetchone()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No resources found for user ID {user_id}",
                )

            # Actualizar los recursos
            updated_result = con.execute(
                update_query,
                {
                    "user_id": user_id,
                    "food": update.food,
                    "gold": update.gold,
                    "wood": update.wood,
                    "stone": update.stone,
                },
            ).fetchone()

            con.commit()

            # Devolver los datos actualizados
            return UserResourceResponse(
                id=updated_result.id,
                user_id=updated_result.user_id,
                food=updated_result.food,
                gold=updated_result.gold,
                wood=updated_result.wood,
                stone=updated_result.stone,
            )
        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while updating resources: {str(e)}",
            )
