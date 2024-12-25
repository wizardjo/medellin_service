# Función para crear una conexión a la base de datos
from datetime import datetime, timedelta
from fastapi import Depends
import jwt
from passlib.context import CryptContext

# Configuración de seguridad
SECRET_KEY = "your-secret-key"  # Cambia esto por una clave secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar y crear contraseñas
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Función para generar tokens
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)