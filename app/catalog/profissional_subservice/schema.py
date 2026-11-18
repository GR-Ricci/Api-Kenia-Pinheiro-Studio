from typing import Annotated
from pydantic import BaseModel, BeforeValidator


def vazio_vira_none(valor):
    if valor == "":
        return None
    return valor


Nullable = Annotated[str | None, BeforeValidator(vazio_vira_none)]


class ProfissionalSubservicoRequest(BaseModel):
    id_subservico: int
    preco: float
    duracao_minutos: int
    imagem_url: Nullable = None
    id_profissional: int | None = None
    descricao: Nullable = None


class ProfissionalSubservicoUpdateRequest(BaseModel):
    preco: float | None = None
    duracao_minutos: int | None = None
    imagem_url: Nullable = None
    ativo: bool | None = None
    descricao: Nullable = None


class ProfissionalSubservicoResponse(BaseModel):
    id_profissional: int
    id_subservico: int
    nome_subservico: str
    nome_servico: str
    nome_categoria: str
    imagem_url: Nullable = None
    preco: float
    duracao_minutos: int
    ativo: bool
    descricao: Nullable = None