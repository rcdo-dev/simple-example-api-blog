from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError

from core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scheme_name="BearerAuth"
)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Gera um token JWT com dados do usuário e tempo de expiração.
    """

    to_encode = data.copy()

    # 1. Definir tempo de expiração (exp)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # 2. Codificar o token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGOTITHM)

    return encoded_jwt

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    """
    Decodifica e valida o JWT, retornando o email do usuário (subject).
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. Decodificar o token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGOTITHM])

        # 2. Extrair o 'subject' (email)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception