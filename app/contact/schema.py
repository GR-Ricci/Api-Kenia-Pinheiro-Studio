# define o formato dos dados que entram e saem da API.


"""
Exemplo de uso:
{
    "imagem_url": "imagem.jpg",
    "ordem_exibicao": 1
}
"""

from pydantic import BaseModel


#Contato do estúdio

class ContatoResponse(BaseModel):
    telefone: str
    whatsapp: str | None
    email: str | None
    rede_social: str | None     #ex: "@keniapinheirostudio"
    endereco: str | None
