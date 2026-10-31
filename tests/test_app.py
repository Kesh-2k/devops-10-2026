"""Testes das rotas da API de tarefas (SQLite em memória)."""

from fastapi.testclient import TestClient

from app.api import APP

CLIENT = TestClient(APP)


def test_index():
    """Rota raiz responde."""
    resposta = CLIENT.get("/")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Olá, mundo!"}


def test_tarefas_get():
    """Lista começa vazia."""
    resposta = CLIENT.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_tarefas_post():
    """Cria uma tarefa e ela aparece na lista."""
    resposta = CLIENT.post("/tarefas?titulo=teste&descricao=teste")
    assert resposta.status_code == 201
    assert resposta.json() == {"mensagem": "OK"}

    lista = CLIENT.get("/tarefas").json()
    assert len(lista) == 1
    assert lista[0]["_id"] == 1
    assert lista[0]["titulo"] == "teste"


def test_tarefa_criada():
    """A tarefa criada tem os dados enviados e não está concluída."""
    resposta = CLIENT.get("/tarefas/1")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["_id"] == 1
    assert dados["titulo"] == "teste"
    assert dados["descricao"] == "teste"
    assert dados["concluida"] is False
    assert dados["data_criacao"]
    assert dados["data_conclusao"] is None


def test_tarefas_put():
    """Concluir uma tarefa existente e uma que não existe."""
    assert CLIENT.put("/tarefas/1").json() == {"mensagem": "Tarefa atualizada"}
    assert CLIENT.put("/tarefas/1").json() == {"mensagem": "Tarefa já finalizada"}
    assert CLIENT.put("/tarefas/2").json() == {"mensagem": "Tarefa não existe"}


def test_tarefas_get_id():
    """Tarefa concluída tem data de conclusão."""
    dados = CLIENT.get("/tarefas/1").json()
    assert dados["concluida"] is True
    assert dados["data_conclusao"] is not None

    assert CLIENT.get("/tarefas/2").json() == {"mensagem": "Tarefa não existe"}


def test_tarefas_delete():
    """Apagar uma tarefa que não existe e a criada."""
    assert CLIENT.delete("/tarefas/2").json() == {"mensagem": "Tarefa não existe"}
    assert CLIENT.delete("/tarefas/1").json() == {"mensagem": "Tarefa removida"}
    assert CLIENT.get("/tarefas").json() == []


def test_autor():
    """Rota do autor."""
    resposta = CLIENT.get("/autor")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Pedro Rocha Horchulhack"}
