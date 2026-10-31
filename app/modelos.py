"""Modelos da aplicação de tarefas"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Tarefa(SQLModel, table=True):
    """Modelo de tarefa"""

    id: int | None = Field(alias="_id", primary_key=True, unique=True, default=None)
    titulo: str
    descricao: str | None = None
    concluida: bool = False
    data_criacao: datetime
    data_conclusao: datetime | None = None

    def finalizar(self):
        """Método para finalizar tarefa"""
        self.concluida = True
        self.data_conclusao = datetime.now().astimezone(UTC)

    def resumir(self):
        """Resume tarefa em `id: titulo`"""
        return {self.id: self.titulo}

    def get_id(self):
        """Retorna ID da tarefa"""
        return self.id
