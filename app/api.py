"""Aplicação para o módulo de extensão DevOps"""

import os
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from .modelos import Tarefa


def criar_engine():
    """Cria a conexão com o banco.

    Ordem: DATABASE_URL; senão MySQL com DATABASE_USERNAME, DATABASE_PASSWORD,
    DATABASE_ADDRESS e DATABASE; senão SQLite em memória (testes e desenvolvimento).
    """
    url = os.environ.get("DATABASE_URL")
    if url:
        return create_engine(url)

    nomes = ("DATABASE_USERNAME", "DATABASE_PASSWORD", "DATABASE_ADDRESS", "DATABASE")
    valores = [os.environ.get(nome) for nome in nomes]
    if all(valores):
        usuario, senha, endereco, banco = valores
        porta = os.environ.get("DATABASE_PORT", "3306")
        return create_engine(f"mysql+pymysql://{usuario}:{senha}@{endereco}:{porta}/{banco}")

    faltando = [nome for nome, valor in zip(nomes, valores) if not valor]
    print(f"Variáveis do banco ausentes ({', '.join(faltando)}): usando SQLite em memória.")
    return create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


ENGINE = criar_engine()
SQLModel.metadata.create_all(ENGINE)


def criar_sessao():
    """Abre uma sessão do banco por requisição."""
    with Session(ENGINE) as s:
        yield s


SESSAO = Annotated[Session, Depends(criar_sessao)]

APP = FastAPI()


# GET /tarefas: Lista todas as tarefas
@APP.get("/tarefas")
async def tarefas(sessao: SESSAO) -> list[Tarefa]:
    """Rota para listar as tarefas."""
    return sessao.exec(select(Tarefa)).all()


# POST /tarefas: Cria tarefa
@APP.post("/tarefas", status_code=201)
async def post_tarefa(sessao: SESSAO, titulo: str, descricao: str | None = None):
    """Rota para criar uma tarefa."""
    tarefa_nova = Tarefa(
        titulo=titulo,
        descricao=descricao,
        data_criacao=datetime.now(UTC),
    )

    sessao.add(tarefa_nova)
    sessao.commit()
    sessao.refresh(tarefa_nova)

    return {"mensagem": "OK"}


# GET /tarefas/{id_tarefa}: Visualizar tarefa específica
@APP.get("/tarefas/{id_tarefa}", response_model=None)
async def tarefa_especifica(sessao: SESSAO, id_tarefa: int) -> Tarefa | dict:
    """Rota para visualizar uma tarefa específica"""
    tarefa = sessao.get(Tarefa, id_tarefa)
    if tarefa:
        return tarefa
    return {"mensagem": "Tarefa não existe"}


# PUT /tarefas/{id}: Conclui tarefa específica
@APP.put("/tarefas/{id_tarefa}")
async def concluir_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para concluir uma tarefa."""
    tarefa = sessao.get(Tarefa, id_tarefa)

    if not tarefa:
        return {"mensagem": "Tarefa não existe"}

    if tarefa.concluida:
        return {"mensagem": "Tarefa já finalizada"}

    tarefa.finalizar()

    sessao.add(tarefa)
    sessao.commit()
    sessao.refresh(tarefa)

    return {"mensagem": "Tarefa atualizada"}


# DELETE /tarefas/{id_tarefa}: Exclui tarefa
@APP.delete("/tarefas/{id_tarefa}")
async def apagar_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para apagar tarefa."""
    tarefa = sessao.get(Tarefa, id_tarefa)

    if not tarefa:
        return {"mensagem": "Tarefa não existe"}

    sessao.delete(tarefa)
    sessao.commit()

    return {"mensagem": "Tarefa removida"}


@APP.get("/")
async def index():
    """Rota raíz."""
    return {"mensagem": "Olá, mundo!"}


@APP.get("/autor")
async def autor():
    """Rota para retornar o autor da aplicação"""
    return {"mensagem": "Pedro Rocha Horchulhack"}
