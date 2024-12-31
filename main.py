import os
import jwt
import psycopg2

from datetime import timedelta
from typing import List
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from authentication.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    verify_password,
)
from db import database
from db.database import engine
from routes import users, buildings, celebrations, characters, missions
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
app.include_router(buildings.router)
app.include_router(celebrations.router)
app.include_router(characters.router)
app.include_router(missions.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
database.Base.metadata.create_all(bind=engine)


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
