from pydantic import BaseModel


class HomeResponse(BaseModel):
    imagem_url: str | None = None
    atualizado_em: int | None = None