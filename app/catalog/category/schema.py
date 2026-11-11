from pydantic import BaseModel


class CategoryRequest(BaseModel):
    nome: str


class CategoryUpdateRequest(BaseModel):
    nome: str
    ativo: bool = True


class CategoryResponse(BaseModel):
    id: int
    nome: str
    ativo: bool


class CategoryDeleteCheckResponse(BaseModel):
    pode_deletar: bool
    profissionais_afetadas: int
    servicos_afetados: int
    subservicos_afetados: int