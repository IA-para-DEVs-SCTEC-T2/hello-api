# Spec: Integração com Banco de Dados

## Objetivo
Migrar o armazenamento em memória para um banco de dados persistente (SQLite ou PostgreSQL).

## Requisitos

### 1. Escolha do Banco de Dados
- **Desenvolvimento**: SQLite (arquivo local)
- **Produção**: PostgreSQL (recomendado)

### 2. ORM
- Usar SQLAlchemy como ORM
- Implementar modelos de dados
- Configurar migrations com Alembic

### 3. Estrutura de Dados

#### Tabela: alunos
```sql
CREATE TABLE alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    idade INTEGER NOT NULL CHECK (idade >= 1 AND idade <= 150),
    curso VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Dependências Necessárias
```toml
dependencies = [
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "psycopg2-binary>=2.9.0",  # Para PostgreSQL
]
```

### 5. Configuração

#### database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./alunos.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### models.py
```python
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class AlunoModel(Base):
    __tablename__ = "alunos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    curso = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 6. Atualizar Endpoints
- Substituir `alunos_db` por queries do banco
- Usar `Depends(get_db)` para injeção de dependência
- Implementar tratamento de erros de banco

### 7. Migrations
```bash
# Inicializar Alembic
alembic init alembic

# Criar migration
alembic revision --autogenerate -m "Create alunos table"

# Aplicar migration
alembic upgrade head
```

## Tarefas

- [ ] Instalar dependências (SQLAlchemy, Alembic)
- [ ] Criar database.py com configuração
- [ ] Criar models.py com modelo Aluno
- [ ] Configurar Alembic para migrations
- [ ] Criar migration inicial
- [ ] Atualizar endpoints para usar banco de dados
- [ ] Atualizar testes
- [ ] Atualizar documentação
- [ ] Testar com SQLite
- [ ] Testar com PostgreSQL

## Critérios de Aceitação
- ✅ Dados persistem após reiniciar a aplicação
- ✅ Migrations funcionam corretamente
- ✅ Todos os endpoints continuam funcionando
- ✅ Validações de email único funcionam no banco
- ✅ Performance adequada para operações CRUD
