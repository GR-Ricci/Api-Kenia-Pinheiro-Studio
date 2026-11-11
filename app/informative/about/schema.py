from pydantic import BaseModel


class ContatoUpdate(BaseModel):
    telefone: str | None = None
    whatsapp: str | None = None
    email: str | None = None
    rede_social: str | None = None
    endereco: str | None = None


class ContatoResponse(BaseModel):
    id: int
    telefone: str | None = None
    whatsapp: str | None = None
    email: str | None = None
    rede_social: str | None = None
    endereco: str | None = None