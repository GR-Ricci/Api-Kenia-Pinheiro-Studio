from pydantic import BaseModel

class StaffResponse(BaseModel):
    id: int
    id_profissional: int | None = None
    nome: str
    email: str
    tipo: str
    ativo: bool
    imagem_url: str | None = None
    bio: str | None = None
    superadmin: bool | None = None

class StaffStatusRequest(BaseModel):
    ativo: bool