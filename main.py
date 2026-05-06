import os
from datetime import datetime, timedelta
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
PROFESSOR_USERNAME: str = os.getenv("PROFESSOR_USERNAME")
PROFESSOR_PASSWORD: str = os.getenv("PROFESSOR_PASSWORD")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------

app = FastAPI(
    title="API de Cadastro de Alunos",
    description="API REST para gerenciar cadastro de alunos com operações CRUD completas e autenticação JWT",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------------------

class Token(BaseModel):
    """Token JWT retornado após autenticação."""

    access_token: str
    token_type: str


class Aluno(BaseModel):
    """Representa um aluno cadastrado no sistema."""

    id: Optional[int] = Field(None, description="ID único do aluno (gerado automaticamente)")
    nome: str = Field(..., min_length=3, max_length=100, description="Nome completo do aluno")
    idade: int = Field(..., ge=1, le=150, description="Idade do aluno")
    curso: str = Field(..., min_length=3, max_length=100, description="Curso em que o aluno está matriculado")
    email: str = Field(..., description="Email do aluno")

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome": "João Silva",
                "idade": 20,
                "curso": "Engenharia de Software",
                "email": "joao@example.com",
            }
        }
    }


# ---------------------------------------------------------------------------
# Banco de dados em memória
# ---------------------------------------------------------------------------

alunos_db: list[dict] = []
contador_id: int = 1

# ---------------------------------------------------------------------------
# Autenticação
# ---------------------------------------------------------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> bool:
    """Valida as credenciais do professor."""
    if username != PROFESSOR_USERNAME:
        return False
    return verify_password(password, PROFESSOR_PASSWORD)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um token JWT com tempo de expiração."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    payload = {**data.copy(), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Decodifica o token JWT e retorna o usuário autenticado."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise unauthorized
        return username
    except JWTError:
        raise unauthorized

# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _encontrar_aluno(aluno_id: int) -> tuple[int, dict]:
    """Retorna o índice e os dados do aluno, ou lança 404."""
    for i, aluno in enumerate(alunos_db):
        if aluno["id"] == aluno_id:
            return i, aluno
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aluno com ID {aluno_id} não encontrado",
    )


def _email_em_uso(email: str, ignorar_id: Optional[int] = None) -> bool:
    """Verifica se o e-mail já está cadastrado (opcionalmente ignora um ID)."""
    return any(
        a["email"] == email and a["id"] != ignorar_id
        for a in alunos_db
    )

# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.post(
    "/token",
    response_model=Token,
    summary="Login do Professor",
    description="Autentica o professor e retorna um token JWT para operações protegidas.",
    tags=["Autenticação"],
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/alunos",
    response_model=List[Aluno],
    summary="Listar todos os alunos",
    description="Retorna uma lista com todos os alunos cadastrados no sistema.",
    tags=["Alunos"],
)
def listar_alunos():
    return alunos_db


@app.get(
    "/alunos/{aluno_id}",
    response_model=Aluno,
    summary="Obter aluno por ID",
    description="Retorna os dados de um aluno específico pelo seu ID.",
    responses={
        200: {"description": "Aluno encontrado com sucesso"},
        404: {"description": "Aluno não encontrado"},
    },
    tags=["Alunos"],
)
def obter_aluno(aluno_id: int = Path(..., description="ID do aluno a ser buscado", ge=1)):
    _, aluno = _encontrar_aluno(aluno_id)
    return aluno


@app.post(
    "/alunos",
    response_model=Aluno,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo aluno",
    description="Cria um novo aluno no sistema com os dados fornecidos.",
    responses={
        201: {"description": "Aluno criado com sucesso"},
        422: {"description": "Dados inválidos"},
    },
    tags=["Alunos"],
)
def criar_aluno(aluno: Aluno):
    global contador_id

    if _email_em_uso(aluno.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado no sistema",
        )

    novo_aluno = {**aluno.model_dump(), "id": contador_id}
    contador_id += 1
    alunos_db.append(novo_aluno)
    return novo_aluno


@app.put(
    "/alunos/{aluno_id}",
    response_model=Aluno,
    summary="Atualizar aluno",
    description="Atualiza todos os dados de um aluno existente.",
    responses={
        200: {"description": "Aluno atualizado com sucesso"},
        404: {"description": "Aluno não encontrado"},
        422: {"description": "Dados inválidos"},
    },
    tags=["Alunos"],
)
def atualizar_aluno(
    aluno_id: int = Path(..., description="ID do aluno a ser atualizado", ge=1),
    aluno: Aluno = None,
):
    if _email_em_uso(aluno.email, ignorar_id=aluno_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado para outro aluno",
        )

    i, _ = _encontrar_aluno(aluno_id)
    aluno_atualizado = {**aluno.model_dump(), "id": aluno_id}
    alunos_db[i] = aluno_atualizado
    return aluno_atualizado


@app.delete(
    "/alunos/{aluno_id}",
    summary="Deletar aluno (Apenas Professor)",
    description="Remove um aluno do sistema pelo seu ID. Requer autenticação como professor.",
    responses={
        200: {"description": "Aluno deletado com sucesso"},
        401: {"description": "Não autenticado"},
        404: {"description": "Aluno não encontrado"},
    },
    tags=["Alunos"],
)
def deletar_aluno(
    aluno_id: int = Path(..., description="ID do aluno a ser deletado", ge=1),
    current_user: str = Depends(get_current_user),
):
    i, aluno = _encontrar_aluno(aluno_id)
    alunos_db.pop(i)
    return {
        "mensagem": "Aluno deletado com sucesso",
        "aluno": aluno,
        "deletado_por": current_user,
    }
