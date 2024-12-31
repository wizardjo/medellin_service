from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import text
from db.database import engine
from schemas.schemas import (
    CharacterRequest,
    CharacterResponse,
)

router = APIRouter()


# CHARACTERS start endpoints Characters
# POST Characters
# This method create a new Character
# The parameter is post_Characters: CharactersRequest
@router.post(
    "/characters",
    status_code=status.HTTP_201_CREATED,
    response_model=CharacterResponse,
    tags=["Characters"],
)
def create_character(post_character: CharacterRequest):
    # Consulta SQL segura con parámetros
    query = text(
        "INSERT INTO characters (name, description) VALUES (:name, :description) RETURNING id"
    )
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(
                query,
                {
                    "name": post_character.name,
                    "description": post_character.description,
                },
            )

            # Obtenemos el ID generado por la base de datos
            character_id = result.scalar()
            con.commit()

            # Devolvemos el nuevo objeto de misión con el ID asignado
            new_character = CharacterResponse(
                id=character_id,
                name=post_character.name,
                description=post_character.description,
            )
            return new_character

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating the character: {str(e)}",
            )


# GET character
# This method in the characters route searchs character's id
# The param is Character id
@router.get(
    "/characters/{character_id}",
    status_code=status.HTTP_200_OK,
    response_model=CharacterResponse,
    tags=["Characters"],
)
def get_character(character_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("SELECT * from characters WHERE id=:id")
    with engine.connect() as con:
        # Ejecutamos la consulta con parámetros para evitar inyección SQL
        result = con.execute(query, {"id": character_id}).fetchone()

        if result is None:  # Si no se encuentra el personaje
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Character with id {character_id} not found",
            )

        # El resultado como JSON
        return result


# GET All character
# This method get all characters
@router.get(
    "/characters",
    status_code=status.HTTP_200_OK,
    response_model=List[CharacterResponse],
    tags=["Characters"],
)
def get_all_characters():
    query = text("SELECT * from characters")
    with engine.connect() as con:
        # Ejecutamos la consulta
        results = con.execute(query).fetchall()

        if not results:  # Si no hay personajes
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
            )
        return results


# DELETE
# This method DELETE the character by ID
# The param is character_id
@router.delete(
    "/characters/{character_id}",
    status_code=status.HTTP_200_OK,
    response_model=CharacterResponse,
    tags=["Characters"],
)
def delete_build(character_id: int):
    # Consulta SQL segura utilizando parámetros
    query = text("DELETE FROM characters WHERE id = :id")
    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(query, {"id": character_id})

            # Confirmamos que se eliminó al menos una fila
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Character with id {character_id} not found",
                )

            con.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while deleting the character: {str(e)}",
            )


# end character
