# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter, HTTPException

from service.schema import CategoriaResponse, ServicoResponse, ProfissionalServicoResponse
from service import service


router = APIRouter(tags=["Service"])


@router.get("/categories", response_model=list[CategoriaResponse])
def listar_categorias():                                    #botões de filtro da página de serviços
    return service.listar_categorias()


@router.get("/services", response_model=list[ServicoResponse])
def listar_servicos(id_categoria: int | None = None):      #?id_categoria=1 filtra por categoria
    return service.listar_servicos(id_categoria)


@router.get("/services/{id_servico}/employees", response_model=list[ProfissionalServicoResponse])
def listar_profissionais_do_servico(id_servico: int):      #ao clicar no serviço: quem atende e por quanto
    try:
        return service.listar_profissionais_do_servico(id_servico)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
