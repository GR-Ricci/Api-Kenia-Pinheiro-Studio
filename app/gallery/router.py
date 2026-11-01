# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter

from gallery.schema import TagResponse, GaleriaResponse
from gallery import service


router = APIRouter(tags=["Gallery"])


@router.get("/gallery/tags", response_model=list[TagResponse])
def listar_tags():                                          #botões de filtro da galeria
    return service.listar_tags()


@router.get("/gallery", response_model=list[GaleriaResponse])
def listar_galeria():                                       #fotos, cada uma com as tags dela
    return service.listar_galeria()
