# define o formato dos dados que entram e saem da API.


"""
Exemplo de uso:
{
    "imagem_url": "imagem.jpg",
    "ordem_exibicao": 1
}
"""

from pydantic import BaseModel


#Categoria

class CategoriaResponse(BaseModel):
    id: int
    nome: str

#Serviço

class ServicoResponse(BaseModel):
    id: int
    id_categoria: int
    nome: str
    descricao: str | None
    imagem_url: str | None

#Profissionais de um serviço

class SubservicoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    duracao_minutos: int
    descricao: str | None       #descrição e imagem são da profissional para esse subserviço
    imagem_url: str | None

class ProfissionalServicoResponse(BaseModel):
    id: int
    nome: str
    imagem_url: str | None
    subservicos: list[SubservicoResponse]
