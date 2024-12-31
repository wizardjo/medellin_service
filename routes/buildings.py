from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import text
from db.database import engine
from schemas.schemas import (
    BuildRequest,
    BuildResponse,
)

router = APIRouter()

# BUILDINGS start endpoint
# POST buildings
# This method create a new BUILD
# The parameter is post_build: BuildRequest
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


@router.post(
    "/buildings",
    status_code=status.HTTP_201_CREATED,
    response_model=BuildResponse,
    tags=["Buildings"],
)
def create_build(post_build: BuildRequest):
    # Consulta SQL segura con parámetros
    query = text(
        "INSERT INTO buildings (name, description, cost, preview_build, experience_require) "
        "VALUES (:name, :description, :cost, :preview_build, :experience_require) RETURNING id"
    )
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(
                query,
                {
                    "name": post_build.name,
                    "description": post_build.description,
                    "cost": post_build.cost,
                    "preview_build": post_build.preview_build,
                    "experience_require": post_build.experience_require,
                },
            )

            # Obtenemos el ID generado por la base de datos
            build_id = (
                result.scalar()
            )  # Puede ser None si la consulta falla en retornar un valor
            if not build_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve the generated ID for the new build.",
                )

            con.commit()

            # Devolvemos el nuevo objeto de edificio con el ID asignado
            new_build = BuildResponse(
                id=build_id,
                name=post_build.name,
                cost=post_build.cost,
                description=post_build.description,
                preview_build=post_build.preview_build,
                experience_require=post_build.experience_require,
            )
            return new_build

        except SQLAlchemyError as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )
        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}",
            )


# GET BUILD
# This method in the users route searchs build's id
# The param is build id
@router.get(
    "/buildings/{build_id}",
    status_code=status.HTTP_200_OK,
    response_model=BuildResponse,
    tags=["Buildings"],
)
def get_build(build_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("SELECT * from buildings WHERE id=:id")
    with engine.connect() as con:
        # Ejecutamos la consulta con parámetros para evitar inyección SQL
        result = con.execute(query, {"id": build_id}).fetchone()

        if result is None:  # Si no se encuentra el edificio
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Build with id {build_id} not found",
            )

        return result


# GET ALL BUILDING
# This method get all buildings
@router.get(
    "/buildings",
    status_code=status.HTTP_200_OK,
    response_model=List[BuildResponse],
    tags=["Buildings"],
)
def get_all_buildings():
    query = text("SELECT * FROM buildings")
    with engine.connect() as con:
        # Ejecutamos la consulta
        results = con.execute(query).fetchall()

        if not results:  # Si no hay edificios
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No buildings found"
            )

        return results


# DELETE
# This method DELETE the build by ID
# The param is build_id
@router.delete(
    "/buildings/{build_id}",
    status_code=status.HTTP_200_OK,
    response_model=BuildResponse,
    tags=["Buildings"],
)
def delete_build(build_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("DELETE FROM buildings WHERE id = :id")
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(query, {"id": build_id})

            # Confirmamos que se eliminó al menos una fila
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Build with id {build_id} not found",
                )

            con.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while deleting the build: {str(e)}",
            )


# end build
