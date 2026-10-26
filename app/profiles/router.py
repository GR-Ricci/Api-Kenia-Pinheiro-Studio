# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter, HTTPException, Depends

from auth import validar_token
from profiles.schema import ProfileResponse, ProfileUpdate, ProfileCreate
from profiles import service

router = APIRouter(tags=["Profile"])

@router.get("/profile", response_model=ProfileResponse)
def ver_meu_perfil(usuario_logado = Depends(validar_token)):  #funcao validar token e return no usuario_logado
    try:
        return service.obter_perfil(usuario_logado["id"])

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.post("/profile", response_model=ProfileResponse)
def adicionar_perfil(dados: ProfileCreate, usuario_logado = Depends(validar_token)):

    try:
        return service.post_perfil(usuario_logado["id"], dados)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

@router.patch("/profile", response_model=ProfileUpdate)
def atualizar_perfil(dados: ProfileUpdate, usuario_logado = Depends(validar_token)):

    try:
        return service.update_perfil(usuario_logado["id"], dados)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))