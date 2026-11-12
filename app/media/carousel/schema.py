from pydantic import BaseModel


class CarouselRequest(BaseModel):
    imagem_url: str
    id_categoria: int
    ordem_exibicao: int | None = None


class CarouselUpdateRequest(BaseModel):
    id_categoria: int | None = None
    ordem_exibicao: int | None = None


class CarouselResponse(BaseModel):
    id: int
    imagem_url: str
    id_categoria: int
    nome_categoria: str | None = None
    ordem_exibicao: int | None = None