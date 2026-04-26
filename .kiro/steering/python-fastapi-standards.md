---
inclusion: auto
---

# Padrões Python e FastAPI

## Convenções de Código Python

### Nomenclatura
- **Classes**: PascalCase (ex: `AlunoModel`, `UserService`)
- **Funções e variáveis**: snake_case (ex: `criar_aluno`, `usuario_id`)
- **Constantes**: UPPER_SNAKE_CASE (ex: `SECRET_KEY`, `MAX_ATTEMPTS`)
- **Arquivos**: snake_case (ex: `main.py`, `user_service.py`)

### Type Hints
- Sempre use type hints em funções e métodos
- Use tipos do módulo `typing` quando necessário (List, Dict, Optional, etc.)

```python
def criar_aluno(nome: str, idade: int) -> dict:
    return {"nome": nome, "idade": idade}
```

### Docstrings
- Use docstrings em todas as funções, classes e módulos
- Formato: Google Style ou NumPy Style

```python
def autenticar_usuario(username: str, password: str) -> bool:
    """
    Autentica um usuário com username e senha.
    
    Args:
        username: Nome de usuário
        password: Senha em texto plano
        
    Returns:
        True se autenticado, False caso contrário
    """
    pass
```

## Padrões FastAPI

### Estrutura de Endpoints
- Use tags para organizar endpoints relacionados
- Adicione summary e description em cada endpoint
- Documente responses esperadas (200, 400, 404, etc.)

```python
@app.post(
    "/alunos",
    response_model=Aluno,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo aluno",
    description="Cria um novo aluno no sistema",
    tags=["Alunos"]
)
def criar_aluno(aluno: Aluno):
    pass
```

### Validação com Pydantic
- Use Field para adicionar validações e descrições
- Adicione exemplos nos modelos

```python
class Aluno(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    idade: int = Field(..., ge=1, le=150)
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Silva",
                "idade": 20
            }
        }
```

### Tratamento de Erros
- Use HTTPException para erros HTTP
- Sempre forneça mensagens descritivas

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Aluno com ID {aluno_id} não encontrado"
)
```

### Segurança
- Nunca exponha SECRET_KEY ou credenciais no código
- Use variáveis de ambiente (.env)
- Implemente autenticação JWT para operações sensíveis
- Use HTTPS em produção

## Boas Práticas

### Organização de Código
- Separe modelos, rotas e lógica de negócio
- Use dependency injection do FastAPI
- Mantenha funções pequenas e focadas

### Performance
- Use async/await quando possível
- Implemente paginação para listas grandes
- Use cache quando apropriado

### Testes
- Escreva testes para todos os endpoints
- Use pytest e httpx para testes
- Teste casos de sucesso e erro
