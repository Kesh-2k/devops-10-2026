"""Testes do serviço de notificações."""

from fastapi.testclient import TestClient

from app.notificacoes import NOTIFICACAO

CLIENT = TestClient(NOTIFICACAO)


def test_notificar():
    """Notificar uma tarefa finalizada responde OK."""
    resposta = CLIENT.post("/notificar?_id=1&titulo=teste")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "OK"}
