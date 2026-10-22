# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter, HTTPException

from invite.schema import ConviteRequest, CadastroRequest, ConviteResponse, CadastroResponse
from invite import service


router = APIRouter(tags=["Invite"])


@router.post("/invites", response_model=ConviteResponse)
def criar_convite(dados: ConviteRequest):             #dados = nome variavel   /  conviteRequest = nome schema
    try:
        return service.gerar_convite(dados.tipo)      #dado.tipo  = variavel
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/invites/{token}")
def validar_convite(token: str):
    return service.validar_token(token)

@router.post("/cadastro", response_model=CadastroResponse)
def cadastrar(dados: CadastroRequest):
    try:
        return service.cadastro(dados.token, dados.senha, dados.email)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))