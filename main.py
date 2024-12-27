import os
from datetime import datetime, timedelta
from typing import List
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import jwt
import psycopg2
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from passlib.hash import bcrypt  # Para hashear contraseñas
from fastapi import APIRouter

from authentication.auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, create_access_token, verify_password
from buildings.build import Build
from celebrations.celebration import Celebration
from charaters.character import Character
from db import database
from db.database import engine, get_db
from missions.mission import Mission
from routes import users
from schemas.schemas import (
    BuildRequest,
    BuildResponse,
    MissionRequest,
    MissionResponse,
    UserRequest,
    UserResponse,
    CharacterRequest,
    CharacterResponse,
    CelebrationRequest,
    CelebrationResponse,
)
from users.user import User

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {"name": "missions", "description": "Operations for missions."},
    {"name": "buildings", "description": "Operations for buildings."},
    {"name": "characters", "description": "Operations for characters."},
    {"name": "celebrations", "description": "Operations for celebrations."},
]

app = FastAPI()

app.include_router(users.router)

database.Base.metadata.create_all(bind=engine)

def get_db_connection():
    conn = psycopg2.connect(os.environ['DB_URL'], cursor_factory=RealDictCursor)
    return conn

# Endpoint para obtener un token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Obtener usuario por nombre
            cur.execute("SELECT * FROM users WHERE email = %s", (form_data.username,))
            user = cur.fetchone()
            if not user or not verify_password(form_data.password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            # Crear un token de acceso
            access_token = create_access_token(
                data={"sub": user["email"]},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )
    return {"access_token": access_token, "token_type": "bearer"}

# MISSIONS start missions endpoint
# POST MISSIONS
# This method create a new mission
# The parameter is post_mission: MissionRequest
@app.post(
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
@app.get(
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
@app.get(
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
@app.delete(
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


# BUILDINGS start endpoint
# POST buildings
# This method create a new BUILD
# The parameter is post_build: BuildRequest
from fastapi import HTTPException, status, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

@app.post(
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
            build_id = result.scalar()  # Puede ser None si la consulta falla en retornar un valor
            if not build_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve the generated ID for the new build."
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
@app.get(
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
@app.get(
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
@app.delete(
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


# CHARACTERS start endpoints Characters
# POST Characters
# This method create a new Character
# The parameter is post_Characters: CharactersRequest
@app.post(
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
@app.get(
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
@app.get(
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
@app.delete(
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


# Celebration start endpoints Characters
# POST celebration
# This method create a new celebration
# The parameter is post_celebrationrs: CelebrationsRequest
@app.post(
    "/celebrations",
    status_code=status.HTTP_201_CREATED,
    response_model=CelebrationResponse,
    tags=["Celebrations"],
)
def create_celebration(
    post_celebration: CelebrationRequest
):
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
@app.get(
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
@app.get(
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
@app.delete(
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
