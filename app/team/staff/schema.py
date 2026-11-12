from pydantic import BaseModel


class StaffResponse(BaseModel):
    id: int  # usuario.id
    id_profissional: int | None = None
    nome: str
    email: str
    tipo: str
    ativo: bool
    imagem_url: str | None = None


class StaffStatusRequest(BaseModel):
    ativo: bool