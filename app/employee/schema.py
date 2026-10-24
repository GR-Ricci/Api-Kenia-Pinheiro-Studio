# define o formato dos dados que entram e saem da API.


"""
Exemplo de uso:
{
    "imagem_url": "imagem.jpg",
    "ordem_exibicao": 1
}
"""

from pydantic import BaseModel
from datetime import time


#Jornada

class JornadaResponse(BaseModel):
    dia_semana: int             #0 = domingo ... 6 = sábado
    hora_inicio: time
    hora_fim: time

#Card do funcionário

class ProfissionalCardResponse(BaseModel):
    id: int
    nome: str
    bio: str | None
    imagem_url: str | None
    categorias: list[str]       #ex: ["Cabelos", "Eventos"]
    jornada: list[JornadaResponse]
