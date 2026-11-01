# define o formato dos dados que entram e saem da API.


"""
Exemplo de uso:
{
    "imagem_url": "imagem.jpg",
    "ordem_exibicao": 1
}
"""

from pydantic import BaseModel


#Tag (botões de filtro)

class TagResponse(BaseModel):
    id: int
    nome: str

#Foto da galeria

class GaleriaResponse(BaseModel):
    id: int
    imagem_url: str
    tags: list[str]             #nomes das tags da foto
