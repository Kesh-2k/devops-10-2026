"""Testes para a rota de autoria."""

from fastapi.testclient import TestClient

from app.api import APP

CLIENT = TestClient(APP)


def test_autor():
    """Verifica a resposta da rota de autoria."""
    resposta = CLIENT.get("/autor")

    assert resposta.status_code == 200
    assert resposta.json() == {"Mensagem": "Jeferson de Santana Silva"}
