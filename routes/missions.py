from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import text
from db.database import engine

from schemas.schemas import (
    MissionRequest,
    MissionResponse,
)

router = APIRouter()


# MISSIONS start missions endpoint
# POST MISSIONS
# This method create a new mission
# The parameter is post_mission: MissionRequest
@router.post(
    "/missions",
    status_code=status.HTTP_201_CREATED,
    response_model=MissionResponse,
    tags=["Missions"],
)
def create_mission(post_mission: MissionRequest):
    # Consulta SQL segura con parámetros
    query = text(
        "INSERT INTO missions (name, description) VALUES (:name, :description) RETURNING id"
    )
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(
                query,
                {"name": post_mission.name, "description": post_mission.description},
            )

            # Obtenemos el ID generado por la base de datos
            mission_id = result.scalar()
            con.commit()

            # Devolvemos el nuevo objeto de misión con el ID asignado
            new_mission = MissionResponse(
                id=mission_id,
                name=post_mission.name,
                description=post_mission.description,
            )
            return new_mission

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating the mission: {str(e)}",
            )


# GET ALL MISSIONS
# This method get all missions
@router.get(
    "/missions",
    status_code=status.HTTP_200_OK,
    response_model=List[MissionResponse],
    tags=["Missions"],
)
def get_all_missions():
    query = text("SELECT * from missions")
    with engine.connect() as con:
        # Ejecutamos la consulta
        results = con.execute(query).fetchall()

        if not results:  # Si no hay misiones
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No missions found"
            )

        # resultado
        return results


# GET Mission
# This method in the missions route searchs mission's id
# The param is mission id
@router.get(
    "/missions/{mission_id}",
    status_code=status.HTTP_200_OK,
    response_model=MissionResponse,
    tags=["Missions"],
)
def get_mission(mission_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("SELECT * from missions WHERE id=:id")
    with engine.connect() as con:
        # Ejecutamos la consulta con parámetros para evitar inyección SQL
        result = con.execute(query, {"id": mission_id}).fetchone()

        if result is None:  # Si no se encuentra la mision
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with id {mission_id} not found",
            )

        # retornarlo como JSON
        return result


# DELETE
# This method DELETE the Mission by ID
# The param is mission_id
@router.delete(
    "/missions/{mission_id}",
    status_code=status.HTTP_200_OK,
    response_model=MissionResponse,
    tags=["Missions"],
)
def delete_mission(mission_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("DELETE from missions WHERE id={0}".format(mission_id))
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(query, {"id": mission_id})

            # Confirmamos que se eliminó al menos una fila
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Mission with id {mission_id} not found",
                )

            con.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while deleting the mission: {str(e)}",
            )


# end mission
