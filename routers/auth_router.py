from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import authenticate_user, create_access_token
from config import settings
from models import Token

router = APIRouter(tags=["Autenticação"])


@router.post(
    "/token",
    response_model=Token,
    summary="Login do Professor",
    description="Autentica o professor e retorna um token JWT para operações protegidas.",
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(subject=form_data.username, expires_delta=expires)
    return Token(access_token=access_token, token_type="bearer")
