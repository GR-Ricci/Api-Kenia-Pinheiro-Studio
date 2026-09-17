# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter, HTTPException

from invite.schema import ConviteRequest, CadastroRequest
from invite import service


router = APIRouter(tags=["Invite"])


@router.post("/invites")
def criar_convite(dados: ConviteRequest):
    try:
        return service.gerar_convite(dados.tipo)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/invites/{token}")
def validar_convite(token: str):
    return service.validar_token(token)

@router.post("/cadastro")
def cadastrar(dados: CadastroRequest):
    try:
        return service.cadastro(dados.token, dados.senha, dados.email)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))