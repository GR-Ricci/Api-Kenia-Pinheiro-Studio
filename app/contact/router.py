# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter, HTTPException

from contact.schema import ContatoResponse
from contact import service


router = APIRouter(tags=["Contact"])


@router.get("/contact", response_model=ContatoResponse)
def buscar_contato():                                       #página de contato (os links são montados no site)
    try:
        return service.buscar_contato()
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
