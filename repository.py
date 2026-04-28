from typing import Optional
from models import Aluno, AlunoInput


class AlunoRepository:
    """
    Responsável pelo acesso e persistência dos dados de alunos em memória.
    Segue o princípio de Responsabilidade Única (SRP).
    """

    def __init__(self) -> None:
        self._db: list[dict] = []
        self._counter: int = 1

    def find_all(self) -> list[dict]:
        return self._db

    def find_by_id(self, aluno_id: int) -> Optional[dict]:
        return next((a for a in self._db if a["id"] == aluno_id), None)

    def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        return any(
            a["email"] == email and a["id"] != exclude_id
            for a in self._db
        )

    def create(self, data: AlunoInput) -> dict:
        aluno_dict = data.model_dump()
        aluno_dict["id"] = self._counter
        self._counter += 1
        self._db.append(aluno_dict)
        return aluno_dict

    def update(self, aluno_id: int, data: AlunoInput) -> dict:
        index = next((i for i, a in enumerate(self._db) if a["id"] == aluno_id), None)
        if index is None:
            return None

        aluno_dict = data.model_dump()
        aluno_dict["id"] = aluno_id
        self._db[index] = aluno_dict
        return aluno_dict

    def delete(self, aluno_id: int) -> Optional[dict]:
        index = next((i for i, a in enumerate(self._db) if a["id"] == aluno_id), None)
        if index is None:
            return None
        return self._db.pop(index)


aluno_repository = AlunoRepository()
