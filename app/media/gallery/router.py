from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from media.gallery import service
from media.gallery.schema import (
    GaleriaRequest,
    GaleriaUpdateRequest,
    GaleriaResponse,
)

router = APIRouter(tags=["Gallery"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.post("/galeria", response_model=GaleriaResponse)
def criar_foto(dados: GaleriaRequest, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        return service.criar_foto(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/galeria", response_model=list[GaleriaResponse])
def listar_fotos(usuario_logado=Depends(validar_token)):
    return service.listar_fotos()


@router.put("/galeria/{id_galeria}", response_model=GaleriaResponse)
def atualizar_foto(
    id_galeria: int,
    dados: GaleriaUpdateRequest,
    usuario_logado=Depends(validar_token),
):
    _requer_admin(usuario_logado)
    try:
        return service.atualizar_foto(id_galeria, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/galeria/{id_galeria}")
def remover_foto(id_galeria: int, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        service.remover_foto(id_galeria)
        return {"ok": True}
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))