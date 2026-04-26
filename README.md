# 🎓 API de Cadastro de Alunos

API REST desenvolvida com FastAPI para gerenciar cadastro de alunos. Projeto didático demonstrando conceitos de APIs RESTful, documentação automática com Swagger e containerização com Docker.

## 🚀 Como Rodar a API

### Opção 1: Rodando pelo Terminal (com UV)

1. **Instale o UV** (gerenciador de pacotes Python):
   ```bash
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone o repositório e entre no diretório**:
   ```bash
   git clone https://github.com/IA-para-DEVs-SCTEC-T2/hello-api.git
   cd hello-api
   ```

3. **Crie o ambiente virtual**:
   ```bash
   uv venv
   ```

4. **Instale as dependências**:
   ```bash
   uv pip install fastapi "uvicorn[standard]" python-jose[cryptography] passlib[bcrypt] python-dotenv
   ```

5. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.example .env
   ```

6. **Execute a API**:
   ```bash
   # Windows
   .venv\Scripts\python.exe -m uvicorn main:app --reload
   
   # Linux/macOS
   .venv/bin/python -m uvicorn main:app --reload
   ```

7. **Acesse a documentação**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Opção 2: Rodando com Docker

1. **Build da imagem**:
   ```bash
   docker build -t hello-api .
   ```

2. **Execute o container**:
   ```bash
   docker run -p 8000:8000 hello-api
   ```

3. **Acesse a documentação**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## ✨ Funcionalidades

### Sistema de Autenticação JWT
- Proteção do endpoint DELETE com autenticação JWT
- Login com credenciais do professor
- Tokens de acesso com expiração configurável

**Credenciais padrão:**
- Usuário: `professor`
- Senha: `professor123`

### CRUD Completo de Alunos
- **GET /alunos** - Lista todos os alunos
- **GET /alunos/{id}** - Busca aluno por ID
- **POST /alunos** - Cria novo aluno
- **PUT /alunos/{id}** - Atualiza aluno
- **DELETE /alunos/{id}** - Remove aluno (requer autenticação)

### Validações
- Email único (não permite duplicados)
- Nome e curso com tamanho mínimo/máximo
- Idade entre 1 e 150 anos
- Mensagens de erro descritivas

## 🔧 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **JWT (python-jose)** - Autenticação com tokens
- **Passlib + Bcrypt** - Criptografia de senhas
- **Python-dotenv** - Gerenciamento de variáveis de ambiente
- **Docker** - Containerização

## 📝 Exemplos de Uso

### Autenticação (Login)

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=professor&password=professor123"
```

### Criar um aluno

```bash
curl -X POST "http://localhost:8000/alunos" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "idade": 20,
    "curso": "Engenharia de Software",
    "email": "joao@example.com"
  }'
```

### Listar todos os alunos

```bash
curl -X GET "http://localhost:8000/alunos"
```

### Deletar aluno (com autenticação)

```bash
curl -X DELETE "http://localhost:8000/alunos/1" \
  -H "Authorization: Bearer SEU_TOKEN"
```

## ⚠️ Observações

- Esta é uma API didática que armazena dados em memória
- Os dados são perdidos quando a aplicação é reiniciada
- Para produção, considere usar um banco de dados real (PostgreSQL, MongoDB, etc.)
- O arquivo .env não deve ser versionado em produção (use .env.example como template)

## 📄 Licença

Projeto educacional de código aberto.
