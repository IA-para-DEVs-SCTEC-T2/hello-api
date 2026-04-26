---
inclusion: fileMatch
fileMatchPattern: "Dockerfile|docker-compose.yml|.dockerignore"
---

# Guia Docker

## Dockerfile

### Estrutura Básica
```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system [dependências]
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Boas Práticas
- Use imagens slim para reduzir tamanho
- Copie arquivos de dependências primeiro (cache de layers)
- Use .dockerignore para excluir arquivos desnecessários
- Não inclua .env no build (use .env.example)
- Exponha apenas portas necessárias

## .dockerignore

### Arquivos a Excluir
```
__pycache__/
.venv/
.env
.git/
.kiro/
*.md
.vscode/
.idea/
```

## Comandos Docker

### Build
```bash
# Build básico
docker build -t hello-api .

# Build com tag específica
docker build -t hello-api:v1.0.0 .

# Build sem cache
docker build --no-cache -t hello-api .
```

### Run
```bash
# Run básico
docker run -p 8000:8000 hello-api

# Run com variáveis de ambiente
docker run -p 8000:8000 -e SECRET_KEY=mysecret hello-api

# Run em background
docker run -d -p 8000:8000 hello-api

# Run com volume para desenvolvimento
docker run -p 8000:8000 -v $(pwd):/app hello-api
```

### Gerenciamento
```bash
# Listar containers
docker ps

# Parar container
docker stop <container_id>

# Remover container
docker rm <container_id>

# Ver logs
docker logs <container_id>

# Executar comando no container
docker exec -it <container_id> bash
```

## Docker Compose (Futuro)

### Exemplo com Banco de Dados
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/alunos
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=alunos
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Troubleshooting

### Container não inicia
- Verifique logs: `docker logs <container_id>`
- Verifique se a porta está disponível
- Verifique variáveis de ambiente

### Mudanças não aparecem
- Rebuild a imagem: `docker build --no-cache -t hello-api .`
- Remova containers antigos: `docker rm -f $(docker ps -aq)`

### Performance lenta
- Use volumes para desenvolvimento
- Considere multi-stage builds para produção
- Otimize layers do Dockerfile
