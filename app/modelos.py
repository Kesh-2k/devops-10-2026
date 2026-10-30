from pydantic import BaseModel

class Autor(BaseModel):
    id: int
    nome: str
    email: str
    criado_em: str

class Livro(BaseModel):
    id: int
    titulo: str
    autor_id: int
    publicado_em: str

class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: str
    concluida: bool
    criada_em: str        