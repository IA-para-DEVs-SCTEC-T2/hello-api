# Spec: Suite de Testes

## Objetivo
Implementar testes automatizados completos para garantir qualidade e confiabilidade da API.

## Requisitos

### 1. Framework de Testes
- **pytest**: Framework principal
- **httpx**: Cliente HTTP para testes
- **pytest-cov**: Cobertura de código

### 2. Dependências
```toml
[project.optional-dependencies]
test = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.24.0",
]
```

### 3. Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py          # Fixtures compartilhadas
├── test_auth.py         # Testes de autenticação
├── test_alunos.py       # Testes de CRUD
└── test_validations.py  # Testes de validações
```

### 4. Fixtures (conftest.py)

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    response = client.post(
        "/token",
        data={"username": "professor", "password": "professor123"}
    )
    return response.json()["access_token"]

@pytest.fixture
def aluno_exemplo():
    return {
        "nome": "João Silva",
        "idade": 20,
        "curso": "Engenharia de Software",
        "email": "joao@example.com"
    }
```

### 5. Casos de Teste

#### Autenticação (test_auth.py)
- [ ] Login com credenciais válidas
- [ ] Login com credenciais inválidas
- [ ] Acesso a endpoint protegido sem token
- [ ] Acesso a endpoint protegido com token inválido
- [ ] Acesso a endpoint protegido com token válido
- [ ] Token expirado

#### CRUD de Alunos (test_alunos.py)
- [ ] Listar alunos (lista vazia)
- [ ] Criar aluno com dados válidos
- [ ] Criar aluno com dados inválidos
- [ ] Buscar aluno por ID existente
- [ ] Buscar aluno por ID inexistente
- [ ] Atualizar aluno existente
- [ ] Atualizar aluno inexistente
- [ ] Deletar aluno (com autenticação)
- [ ] Deletar aluno (sem autenticação)

#### Validações (test_validations.py)
- [ ] Email único (não permite duplicados)
- [ ] Nome muito curto (< 3 caracteres)
- [ ] Nome muito longo (> 100 caracteres)
- [ ] Idade inválida (< 1 ou > 150)
- [ ] Curso muito curto
- [ ] Email inválido
- [ ] Campos obrigatórios faltando

### 6. Exemplo de Teste

```python
def test_criar_aluno_sucesso(client, aluno_exemplo):
    response = client.post("/alunos", json=aluno_exemplo)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == aluno_exemplo["nome"]
    assert data["email"] == aluno_exemplo["email"]
    assert "id" in data

def test_email_duplicado(client, aluno_exemplo):
    # Criar primeiro aluno
    client.post("/alunos", json=aluno_exemplo)
    
    # Tentar criar segundo aluno com mesmo email
    response = client.post("/alunos", json=aluno_exemplo)
    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]

def test_deletar_sem_autenticacao(client):
    response = client.delete("/alunos/1")
    assert response.status_code == 401
```

### 7. Comandos

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=. --cov-report=html

# Executar testes específicos
pytest tests/test_auth.py

# Executar com verbose
pytest -v

# Executar e parar no primeiro erro
pytest -x
```

### 8. Configuração (pytest.ini)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers
```

## Tarefas

- [ ] Instalar dependências de teste
- [ ] Criar estrutura de diretórios
- [ ] Implementar fixtures em conftest.py
- [ ] Escrever testes de autenticação
- [ ] Escrever testes de CRUD
- [ ] Escrever testes de validações
- [ ] Configurar pytest.ini
- [ ] Atingir 80%+ de cobertura
- [ ] Documentar como executar testes
- [ ] Integrar com CI/CD (GitHub Actions)

## Critérios de Aceitação
- ✅ Todos os testes passam
- ✅ Cobertura de código >= 80%
- ✅ Testes são rápidos (< 5 segundos)
- ✅ Testes são independentes
- ✅ Documentação clara de como executar
