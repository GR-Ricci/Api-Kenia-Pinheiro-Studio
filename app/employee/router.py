# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter

from employee.schema import ProfissionalCardResponse
from employee import service


router = APIRouter(tags=["Employee"])


@router.get("/employees", response_model=list[ProfissionalCardResponse])
def listar_cards():                     #rota pública: cards da equipe no site
    return service.listar_cards()
