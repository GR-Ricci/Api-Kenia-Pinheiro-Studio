from typing import Annotated
from pydantic import BaseModel, BeforeValidator


def vazio_vira_none(valor):
    if valor == "":
        return None
    return valor


Nullable = Annotated[str | None, BeforeValidator(vazio_vira_none)]


class ServiceRequest(BaseModel):
    nome: str
    id_categoria: int
    imagem_url: Nullable = None


class ServiceUpdateRequest(BaseModel):
    nome: str
    id_categoria: int
    imagem_url: Nullable = None
    ativo: bool = True


class ServiceResponse(BaseModel):
    id: int
    nome: str
    id_categoria: int
    imagem_url: Nullable = None
    ativo: bool
    nome_categoria: str | None = None


class ServiceDeleteCheckResponse(BaseModel):
    pode_deletar: bool
    profissionais_afetadas: int
    subservicos_afetados: int