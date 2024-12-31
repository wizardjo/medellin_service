import os
import bcrypt
import psycopg2
import jwt

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from datetime import datetime
from typing import List
from sqlalchemy import text
from psycopg2.extras import RealDictCursor
from passlib.hash import bcrypt  # Para hashear contraseñas
from authentication.auth import ALGORITHM, SECRET_KEY
from schemas.schemas import UserRequest, UserResponse
from users.user import User
from db.database import engine

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db_connection():
    conn = psycopg2.connect(os.environ["DB_URL"], cursor_factory=RealDictCursor)
    return conn


# Dependencia para verificar el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")
                if username is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                    )
                # Verificar si el usuario existe en la base de datos
                cur.execute("SELECT * FROM users WHERE email = %s", (username,))
                user = cur.fetchone()
                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not found",
                    )
                return user
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )


# USER start endpoints user
# POST USER
# This method create a new user
# The parameter is post_user: UserRequest
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    tags=["Users"],
)
def create_user(post_user: UserRequest):
    # Hasheamos la contraseña antes de guardarla
    hashed_password = bcrypt.hash(post_user.password)

    # Consulta SQL usando parámetros para PostgreSQL
    query = text(
        """
        INSERT INTO users (name, email, password, registerdatetime) 
        VALUES (:name, :email, :password, :registerdatetime)
        RETURNING id
    """
    )

    with engine.connect() as con:
        try:
            # Verificamos si el email ya existe
            email_check_query = text("SELECT id FROM users WHERE email = :email")
            existing_user = con.execute(
                email_check_query, {"email": post_user.email}
            ).fetchone()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use",
                )

            # Insertamos al nuevo usuario y obtenemos el ID generado
            result = con.execute(
                query,
                {
                    "name": post_user.name,
                    "email": post_user.email,
                    "password": hashed_password,  # Usamos la contraseña hasheada
                    "registerdatetime": str(datetime.now()),
                },
            )
            user_id = result.fetchone()[0]
            con.commit()

            # Creamos y retornamos el objeto usuario
            new_user = User(**post_user.model_dump())
            new_user.id = user_id
            return new_user

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating user: {str(e)}",
            )


# GET USER
# This method in the users route searchs user's id
# The param is user id
@router.get(
    "/users/{email}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    tags=["Users"],
)
def get_user(email: str, current_user: dict = Depends(get_current_user)):
    # Consulta SQL segura utilizando parámetros
    query = text("SELECT * FROM users WHERE email = :email")

    with engine.connect() as con:
        # Ejecutamos la consulta con parámetros para evitar inyección SQL
        result = con.execute(query, {"email": email}).fetchone()

        if result is None:  # Si no se encuentra el usuario
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {email} not found",
            )

        #  retornarlo como JSON
        return result


# GET ALL USERS
# This method get all user
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse],
    tags=["Users"],
)
def get_all_users(current_user: dict = Depends(get_current_user)):
    # Consulta SQL segura
    query = text("SELECT * FROM users")

    with engine.connect() as con:
        # Ejecutamos la consulta
        results = con.execute(query).fetchall()

        if not results:  # Si no hay usuarios
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
            )

        # Convertimos los resultados a una lista de diccionarios
        return results


# DELETE
# This method DELETE the user by ID
# The param is user_id
@router.delete(
    "/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"]
)
def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    # Consulta SQL segura utilizando parámetros
    query = text("DELETE FROM users WHERE id = :id")

    with engine.connect() as con:
        try:
            # Ejecutamos la consulta con parámetros
            result = con.execute(query, {"id": user_id})

            # Confirmamos que se eliminó al menos una fila
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {user_id} not found",
                )

            con.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while deleting the user: {str(e)}",
            )


# end user
