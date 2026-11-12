from typing import Annotated
from pydantic import BaseModel, BeforeValidator, Field


def vazio_vira_none(valor):
    if valor == "":
        return None
    return valor


Nullable = Annotated[str | None, BeforeValidator(vazio_vira_none)]


class PacoteItemRequest(BaseModel):
    id_subservico: int
    quantidade: int = Field(gt=0)


class PacoteRequest(BaseModel):
    id_categoria: int | None = None   # opcional — backend auto-atribui "Pacotes"
    nome: str
    preco: float = Field(gt=0)
    descricao: Nullable = None
    imagem_url: Nullable = None
    ativo: bool = True
    itens: list[PacoteItemRequest] = Field(min_length=1)


class PacoteItemResponse(BaseModel):
    id: int
    id_subservico: int
    nome_subservico: str
    nome_servico: str
    nome_categoria: str
    quantidade: int
    preco_unitario: float
    duracao_minutos: int
    imagem_url: Nullable = None


class PacoteResponse(BaseModel):
    id: int
    id_profissional: int | None = None
    nome_profissional: str | None = None
    imagem_profissional_url: Nullable = None
    id_categoria: int
    nome_categoria: str
    nome: str
    preco: float
    descricao: Nullable = None
    imagem_url: Nullable = None
    ativo: bool
    itens: list[PacoteItemResponse]


class PacoteDeleteCheckResponse(BaseModel):
    pode_deletar: bool
    itens: int
    agendamentos_afetados: int


class SubservicoRapidoRequest(BaseModel):
    nome: str


class SubservicoRapidoResponse(BaseModel):
    id_subservico: int
    nome_subservico: str
    nome_servico: str
    nome_categoria: str