---
inclusion: auto
---

# Guia de Desenvolvimento da API

## Workflow de Desenvolvimento

### 1. Configuração Inicial
```bash
# Criar ambiente virtual
uv venv

# Instalar dependências
uv pip install fastapi "uvicorn[standard]" python-jose[cryptography] passlib[bcrypt] python-dotenv

# Configurar .env
cp .env.example .env
```

### 2. Executar a API
```bash
# Windows
.venv\Scripts\python.exe -m uvicorn main:app --reload

# Linux/macOS
.venv/bin/python -m uvicorn main:app --reload
```

### 3. Testar Endpoints
- Acesse http://localhost:8000/docs para Swagger UI
- Use a interface interativa para testar endpoints
- Para endpoints protegidos, faça login primeiro em /token

## Estrutura da API

### Modelos de Dados
- `Token`: Modelo de resposta de autenticação
- `Aluno`: Modelo principal com validações

### Endpoints Públicos
- `GET /` - Redireciona para documentação
- `POST /token` - Login do professor
- `GET /alunos` - Lista todos os alunos
- `GET /alunos/{id}` - Busca aluno por ID
- `POST /alunos` - Cria novo aluno
- `PUT /alunos/{id}` - Atualiza aluno

### Endpoints Protegidos
- `DELETE /alunos/{id}` - Remove aluno (requer autenticação)

## Autenticação JWT

### Como Funciona
1. Professor faz login em `/token` com username e password
2. API retorna um token JWT
3. Token deve ser incluído no header Authorization: Bearer {token}
4. Token expira após 30 minutos (configurável)

### Credenciais Padrão
- Username: `professor`
- Password: `professor123`

### Gerar Nova Senha Hash
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("sua_senha")
print(hashed)
```

## Validações Implementadas

### Email Único
- Não permite cadastrar dois alunos com o mesmo email
- Verifica na criação e atualização

### Campos Obrigatórios
- Nome: 3-100 caracteres
- Idade: 1-150 anos
- Curso: 3-100 caracteres
- Email: formato válido

## Tratamento de Erros

### Códigos HTTP
- `200 OK` - Operação bem-sucedida
- `201 Created` - Recurso criado
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autenticado
- `404 Not Found` - Recurso não encontrado
- `422 Unprocessable Entity` - Validação falhou

## Docker

### Build
```bash
docker build -t hello-api .
```

### Run
```bash
docker run -p 8000:8000 hello-api
```

## Próximos Passos

### Melhorias Sugeridas
1. Implementar banco de dados persistente (PostgreSQL/SQLite)
2. Adicionar testes automatizados (pytest)
3. Implementar paginação na listagem
4. Adicionar filtros e busca
5. Implementar rate limiting
6. Adicionar logs estruturados
7. Implementar CORS para frontend
