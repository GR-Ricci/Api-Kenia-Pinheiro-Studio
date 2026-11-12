from pydantic import BaseModel


class TagRequest(BaseModel):
    nome: str


class TagResponse(BaseModel):
    id: int
    nome: str