from typing import List
from fastapi import APIRouter, FastAPI, HTTPException, Response, status
from sqlalchemy import text
from schemas.schemas import (
    CelebrationRequest,
    CelebrationResponse,
)
from db.database import engine

router = APIRouter()

# Celebration start endpoints Characters
# POST celebration
# This method create a new celebration
# The parameter is post_celebrationrs: CelebrationsRequest
@router.post(
    "/celebrations",
    status_code=status.HTTP_201_CREATED,
    response_model=CelebrationResponse,
    tags=["Celebrations"],
)
def create_celebration(post_celebration: CelebrationRequest):
    # Consulta SQL segura con parámetros
    query = text(
        "INSERT INTO celebrations (name, description, date) VALUES (:name, :description, :date) RETURNING id"
    )
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(
                query,
                {
                    "name": post_celebration.name,
                    "description": post_celebration.description,
                    "date": post_celebration.date,
                },
            )

            # Obtenemos el ID generado por la base de datos
            build_id = result.scalar()
            con.commit()

            # Devolvemos el nuevo objeto de celebracion con el ID asignado
            new_celebration = CelebrationResponse(
                id=build_id,
                name=post_celebration.name,
                description=post_celebration.description,
                date=post_celebration.date,
            )
            return new_celebration

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating the celebration: {str(e)}",
            )


# GET Celebration
# This method in the Celebration route searchs celebration's id
# The param is celebration id
@router.get(
    "/celebrations/{celebration_id}",
    status_code=status.HTTP_200_OK,
    response_model=CelebrationResponse,
    tags=["Celebrations"],
)
def get_celebration(celebration_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("SELECT * from celebrations WHERE id=:id")
    with engine.connect() as con:
        # Ejecutamos la consulta con parámetros para evitar inyección SQL
        result = con.execute(query, {"id": celebration_id}).fetchone()

        if result is None:  # Si no se encuentra el celebracion
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Celebration with id {celebration_id} not found",
            )

        # JSON
        return result


# GET ALL celebrationS
# This method get all celebrationS
@router.get(
    "/celebrations",
    status_code=status.HTTP_200_OK,
    response_model=List[CelebrationResponse],
    tags=["Celebrations"],
)
def get_all_celebrations():
    query = text("SELECT * from celebrations")
    with engine.connect() as con:
        # Ejecutamos la consulta
        results = con.execute(query).fetchall()

        if not results:  # Si no hay edificios
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No celebrations found"
            )

        return results


# DELETE
# This method DELETE the celebration by ID
# The param is celebration_id
@router.delete(
    "/celebrations/{celebration_id}",
    status_code=status.HTTP_200_OK,
    response_model=CelebrationResponse,
    tags=["Celebrations"],
)
def delete_build(celebration_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("DELETE FROM celebrations WHERE id = :id")
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(query, {"id": celebration_id})

            # Confirmamos que se eliminó al menos una fila
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Celebration with id {celebration_id} not found",
                )

            con.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while deleting the celebration: {str(e)}",
            )


# end celebration
