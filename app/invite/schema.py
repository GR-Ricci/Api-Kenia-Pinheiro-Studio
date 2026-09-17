# define o formato dos dados que entram e saem da API.


"""
Exemplo de uso:
{
    "imagem_url": "imagem.jpg",
    "ordem_exibicao": 1
}
"""

from pydantic import BaseModel
from datetime import datetime


#Convite

class ConviteRequest(BaseModel):
    tipo: str

class ConviteResponse(BaseModel):
    token: str
    link: str
    expira_em: datetime         #apenas para o front mostrar mensagem do tempo

#Validação token

class TokenResponse(BaseModel):
    valido: bool
    tipo: str
    mensagem: str

#Cadastro
from pydantic import EmailStr

class CadastroRequest(BaseModel):
    email : EmailStr
    senha : str
    token : str                 #validacao de token extra (segurança)

class CadastroResponse(BaseModel):
    email : str
    tipo : str
