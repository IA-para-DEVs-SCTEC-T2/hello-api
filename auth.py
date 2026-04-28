from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciais inválidas",
    headers={"WWW-Authenticate": "Bearer"},
)


def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def authenticate_user(username: str, password: str) -> bool:
    """Valida as credenciais do professor."""
    if username != settings.professor_username:
        return False
    return _verify_password(password, settings.professor_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um token JWT com tempo de expiração."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Extrai e valida o usuário a partir do token JWT."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
    except JWTError:
        raise _CREDENTIALS_EXCEPTION

    if username is None:
        raise _CREDENTIALS_EXCEPTION

    return username
