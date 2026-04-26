from fastapi import FastAPI, HTTPException, status, Path, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações de autenticação
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
PROFESSOR_USERNAME = os.getenv("PROFESSOR_USERNAME")
PROFESSOR_PASSWORD = os.getenv("PROFESSOR_PASSWORD")

# Contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="API de Cadastro de Alunos",
    description="API REST para gerenciar cadastro de alunos com operações CRUD completas e autenticação JWT",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos de dados
class Token(BaseModel):
    """Modelo de token JWT."""
    access_token: str
    token_type: str

class Aluno(BaseModel):
    """Modelo de dados para representar um aluno."""
    id: Optional[int] = Field(None, description="ID único do aluno (gerado automaticamente)")
    nome: str = Field(..., min_length=3, max_length=100, description="Nome completo do aluno")
    idade: int = Field(..., ge=1, le=150, description="Idade do aluno")
    curso: str = Field(..., min_length=3, max_length=100, description="Curso em que o aluno está matriculado")
    email: str = Field(..., description="Email do aluno")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Silva",
                "idade": 20,
                "curso": "Engenharia de Software",
                "email": "joao@example.com"
            }
        }

# Banco de dados em memória
alunos_db = []
contador_id = 1

# Funções de autenticação
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> bool:
    """Autentica o usuário professor."""
    if username != PROFESSOR_USERNAME:
        return False
    return verify_password(password, PROFESSOR_PASSWORD)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Valida o token JWT e retorna o usuário."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

@app.get("/", include_in_schema=False)
def root():
    """Redireciona para a documentação Swagger."""
    return RedirectResponse(url="/docs")

@app.post(
    "/token",
    response_model=Token,
    summary="Login do Professor",
    description="Autentica o professor e retorna um token JWT para operações protegidas.",
    tags=["Autenticação"]
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint de login para o professor."""
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get(
    "/alunos",
    response_model=List[Aluno],
    summary="Listar todos os alunos",
    description="Retorna uma lista com todos os alunos cadastrados no sistema.",
    tags=["Alunos"]
)
def listar_alunos():
    """Lista todos os alunos cadastrados."""
    return alunos_db

@app.get(
    "/alunos/{aluno_id}",
    response_model=Aluno,
    summary="Obter aluno por ID",
    description="Retorna os dados de um aluno específico pelo seu ID.",
    responses={
        200: {"description": "Aluno encontrado com sucesso"},
        404: {"description": "Aluno não encontrado"}
    },
    tags=["Alunos"]
)
def obter_aluno(aluno_id: int = Path(..., description="ID do aluno a ser buscado", ge=1)):
    """Busca um aluno específico pelo ID."""
    aluno = next((a for a in alunos_db if a["id"] == aluno_id), None)
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com ID {aluno_id} não encontrado"
        )
    return aluno

@app.post(
    "/alunos",
    response_model=Aluno,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo aluno",
    description="Cria um novo aluno no sistema com os dados fornecidos.",
    responses={
        201: {"description": "Aluno criado com sucesso"},
        422: {"description": "Dados inválidos"}
    },
    tags=["Alunos"]
)
def criar_aluno(aluno: Aluno):
    """Cria um novo aluno no sistema."""
    global contador_id
    
    # Verifica se email já existe
    if any(a["email"] == aluno.email for a in alunos_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado no sistema"
        )
    
    aluno_dict = aluno.model_dump()
    aluno_dict["id"] = contador_id
    contador_id += 1
    alunos_db.append(aluno_dict)
    return aluno_dict

@app.put(
    "/alunos/{aluno_id}",
    response_model=Aluno,
    summary="Atualizar aluno",
    description="Atualiza todos os dados de um aluno existente.",
    responses={
        200: {"description": "Aluno atualizado com sucesso"},
        404: {"description": "Aluno não encontrado"},
        422: {"description": "Dados inválidos"}
    },
    tags=["Alunos"]
)
def atualizar_aluno(
    aluno_id: int = Path(..., description="ID do aluno a ser atualizado", ge=1),
    aluno: Aluno = None
):
    """Atualiza os dados de um aluno existente."""
    for i, a in enumerate(alunos_db):
        if a["id"] == aluno_id:
            # Verifica se email já existe em outro aluno
            if any(a["email"] == aluno.email and a["id"] != aluno_id for a in alunos_db):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado para outro aluno"
                )
            
            aluno_dict = aluno.model_dump()
            aluno_dict["id"] = aluno_id
            alunos_db[i] = aluno_dict
            return aluno_dict
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aluno com ID {aluno_id} não encontrado"
    )

@app.delete(
    "/alunos/{aluno_id}",
    summary="Deletar aluno (Apenas Professor)",
    description="Remove um aluno do sistema pelo seu ID. Requer autenticação como professor.",
    responses={
        200: {"description": "Aluno deletado com sucesso"},
        401: {"description": "Não autenticado"},
        404: {"description": "Aluno não encontrado"}
    },
    tags=["Alunos"]
)
def deletar_aluno(
    aluno_id: int = Path(..., description="ID do aluno a ser deletado", ge=1),
    current_user: str = Depends(get_current_user)
):
    """Remove um aluno do sistema. Apenas o professor pode executar esta operação."""
    for i, a in enumerate(alunos_db):
        if a["id"] == aluno_id:
            aluno_deletado = alunos_db.pop(i)
            return {
                "mensagem": "Aluno deletado com sucesso",
                "aluno": aluno_deletado,
                "deletado_por": current_user
            }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aluno com ID {aluno_id} não encontrado"
    )
