from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import alunos_router, auth_router

app = FastAPI(
    title="API de Cadastro de Alunos",
    description="API REST para gerenciar cadastro de alunos com operações CRUD completas e autenticação JWT",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth_router.router)
app.include_router(alunos_router.router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
