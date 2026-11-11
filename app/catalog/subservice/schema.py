from pydantic import BaseModel


class SubservicoRequest(BaseModel):
    nome: str
    id_servico: int


class SubservicoResponse(BaseModel):
    id: int
    nome: str
    id_servico: int
    ativo: bool
    nome_servico: str | None = None
    nome_categoria: str | None = None