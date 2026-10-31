"""Testes do modelo Tarefa."""

from datetime import UTC, datetime

from app.modelos import Tarefa


def criar_tarefa_mock():
    """Cria uma tarefa de exemplo."""
    return Tarefa(
        id=0,
        titulo="Tarefa teste",
        data_criacao=datetime.now(UTC),
    )


def test_nova_tarefa():
    """Tarefa nova começa sem descrição e não concluída."""
    t = criar_tarefa_mock()

    assert t.get_id() == 0
    assert t.titulo == "Tarefa teste"
    assert t.descricao is None
    assert isinstance(t.data_criacao, datetime)
    assert t.data_conclusao is None
    assert t.concluida is False


def test_tarefa_concluida():
    """Finalizar marca a tarefa como concluída e grava a data."""
    t = criar_tarefa_mock()

    t.finalizar()
    assert t.concluida is True
    assert isinstance(t.data_conclusao, datetime)
    assert t.data_conclusao >= t.data_criacao
