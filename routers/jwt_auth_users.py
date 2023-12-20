from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Definición de constantes
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DURATION = 1  # Duración del token de acceso en minutos
SECRET_KEY = "fb6fc7c074d19811ef7ee8901eddff6dea4645eb918b9c3c0aa91ae5df7b0801"

# Creación de la aplicación FastAPI
router = APIRouter()

# Configuración de seguridad con OAuth2
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

# Contexto de encriptación para contraseñas
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definición de modelo Pydantic para la entrada de usuario en el login
class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

# Definición de modelo Pydantic para el usuario en la base de datos (incluye la contraseña)
class UserDB(User):
    password: str

# Base de datos de usuarios simulada (diccionario)
users_db = {
    "sergio": {
        "username": "sergio",
        "fullname": "Sergio Alexander Huayllas Tirado",
        "email": "sergius16ht@gmail.com",
        "disabled": False,
        "password": "$2a$12$YvHXwhnbydHfvXigHMAUsuvZ5HNmQqJHIS1Kr8j4QkgX/tyR.h.fm"
    },
    "juan": {
        "username": "juan",
        "fullname": "Juan Perez",
        "email": "juan@gmail.com",
        "disabled": True,
        "password": "$2a$12$NE9tHdRnwuk/RTy2eWHoY.82UrY4ReIYER2855BCB83/DazC3f1Um"
    },
}

# Función para buscar un usuario en la base de datos simulada
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Función para buscar un usuario en la base de datos simulada (sin contraseña)
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Función para autenticar al usuario a partir del token de acceso
async def auth_user(token: str = Depends(oauth2)):
    # Excepción para manejar errores de autenticación
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de acceso invalidas",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decodificar el token y obtener el identificador del usuario (sub)
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        # Si el identificador del usuario es nulo, lanzar la excepción
        if username is None:
            raise exception
    except JWTError:
        raise exception

    # Devolver el usuario correspondiente al identificador obtenido del token
    return search_user(username)

# Función para obtener el usuario actual, verificando si está desactivado
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return user

# Ruta para manejar el endpoint de login y emitir tokens de acceso
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Verificar si el usuario existe en la base de datos simulada
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nombre de usuario incorrecto"
        )
    # Buscar al usuario en la base de datos simulada (con contraseña)
    user = search_user_db(form.username)

    # Verificar si la contraseña ingresada coincide con la almacenada en la base de datos
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta"
        )

    # Configurar la expiración del token de acceso
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    # Crear el contenido del token de acceso (sub = identificador del usuario, exp = tiempo de expiración)
    access_token = {
        "sub": user.username,
        "exp": expire
    }

    # Codificar el token de acceso y devolverlo junto con el tipo de token
    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}

# Ruta protegida que devuelve la información del usuario actual
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user