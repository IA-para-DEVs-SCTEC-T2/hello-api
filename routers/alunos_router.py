from fastapi import APIRouter, Depends, HTTPException, Path, status

from auth import get_current_user
from models import Aluno, AlunoInput
from repository import aluno_repository

router = APIRouter(prefix="/alunos", tags=["Alunos"])


def _raise_not_found(aluno_id: int) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aluno com ID {aluno_id} não encontrado",
    )


def _raise_email_conflict(detail: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )


@router.get(
    "",
    response_model=list[Aluno],
    summary="Listar todos os alunos",
    description="Retorna uma lista com todos os alunos cadastrados no sistema.",
)
def listar_alunos() -> list[dict]:
    return aluno_repository.find_all()


@router.get(
    "/{aluno_id}",
    response_model=Aluno,
    summary="Obter aluno por ID",
    description="Retorna os dados de um aluno específico pelo seu ID.",
    responses={
        404: {"description": "Aluno não encontrado"},
    },
)
def obter_aluno(
    aluno_id: int = Path(..., description="ID do aluno a ser buscado", ge=1),
) -> dict:
    aluno = aluno_repository.find_by_id(aluno_id)
    if aluno is None:
        _raise_not_found(aluno_id)
    return aluno


@router.post(
    "",
    response_model=Aluno,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo aluno",
    description="Cria um novo aluno no sistema com os dados fornecidos.",
    responses={
        400: {"description": "Email já cadastrado"},
        422: {"description": "Dados inválidos"},
    },
)
def criar_aluno(aluno: AlunoInput) -> dict:
    if aluno_repository.email_exists(aluno.email):
        _raise_email_conflict("Email já cadastrado no sistema")
    return aluno_repository.create(aluno)


@router.put(
    "/{aluno_id}",
    response_model=Aluno,
    summary="Atualizar aluno",
    description="Atualiza todos os dados de um aluno existente.",
    responses={
        400: {"description": "Email já cadastrado para outro aluno"},
        404: {"description": "Aluno não encontrado"},
        422: {"description": "Dados inválidos"},
    },
)
def atualizar_aluno(
    aluno_id: int = Path(..., description="ID do aluno a ser atualizado", ge=1),
    aluno: AlunoInput = None,
) -> dict:
    if aluno_repository.find_by_id(aluno_id) is None:
        _raise_not_found(aluno_id)

    if aluno_repository.email_exists(aluno.email, exclude_id=aluno_id):
        _raise_email_conflict("Email já cadastrado para outro aluno")

    return aluno_repository.update(aluno_id, aluno)


@router.delete(
    "/{aluno_id}",
    summary="Deletar aluno (Apenas Professor)",
    description="Remove um aluno do sistema pelo seu ID. Requer autenticação como professor.",
    responses={
        401: {"description": "Não autenticado"},
        404: {"description": "Aluno não encontrado"},
    },
)
def deletar_aluno(
    aluno_id: int = Path(..., description="ID do aluno a ser deletado", ge=1),
    current_user: str = Depends(get_current_user),
) -> dict:
    aluno_deletado = aluno_repository.delete(aluno_id)
    if aluno_deletado is None:
        _raise_not_found(aluno_id)

    return {
        "mensagem": "Aluno deletado com sucesso",
        "aluno": aluno_deletado,
        "deletado_por": current_user,
    }
