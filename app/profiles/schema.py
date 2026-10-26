# define o formato dos dados que entram e saem da API.


"""
Exemplo de uso:
{
    "imagem_url": "imagem.jpg",
    "ordem_exibicao": 1
}
"""

from typing import Annotated
from pydantic import BaseModel, BeforeValidator


def vazio_vira_none(valor):
    if valor == "":
        return None
    return valor


# Nullable: string que aceita NULL no banco.
# O BeforeValidator converte "" em None antes de chegar no banco,
# evitando string vazia onde deveria ser NULL.
Nullable = Annotated[str | None, BeforeValidator(vazio_vira_none)]


class ProfileResponse(BaseModel):
    id: int
    nome: str
    bio: Nullable = None
    imagem_url: Nullable = None


class ProfileCreate(BaseModel):
    nome: str
    bio: Nullable = None
    imagem_url: Nullable = None


class ProfileUpdate(BaseModel):
    nome: Nullable = None
    bio: Nullable = None
    imagem_url: Nullable = None

