from pydantic import BaseModel, Field
from typing import Optional


class Token(BaseModel):
    """Representa o token JWT retornado no login."""

    access_token: str
    token_type: str


class AlunoInput(BaseModel):
    """Dados de entrada para criação e atualização de aluno."""

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


class Aluno(AlunoInput):
    """Representa um aluno persistido, com ID gerado automaticamente."""

    id: int = Field(..., description="ID único do aluno")
