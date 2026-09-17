# define o formato dos dados que entram e saem da API.


"""
Exemplo de uso:
{
    "imagem_url": "imagem.jpg",
    "ordem_exibicao": 1
}
"""


from pydantic import BaseModel

class UsuarioEmailResponse(BaseModel):
    id: int
    email: str
