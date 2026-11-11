from pydantic import BaseModel


class TagMini(BaseModel):
    id: int
    nome: str


class GaleriaRequest(BaseModel):
    imagem_url: str
    id_tags: list[int] = []


class GaleriaUpdateRequest(BaseModel):
    imagem_url: str | None = None
    id_tags: list[int] | None = None


class GaleriaResponse(BaseModel):
    id: int
    imagem_url: str
    ordem_exibicao: int | None = None
    tags: list[TagMini] = []