from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from media.carousel import service
from media.carousel.schema import (
    CarouselRequest,
    CarouselUpdateRequest,
    CarouselResponse,
)

router = APIRouter(tags=["Carousel"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.post("/carrossel", response_model=CarouselResponse)
def criar_foto(dados: CarouselRequest, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        return service.criar(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/carrossel", response_model=list[CarouselResponse])
def listar_fotos(usuario_logado=Depends(validar_token)):
    return service.listar()


@router.put("/carrossel/{id_carrossel}", response_model=CarouselResponse)
def atualizar_foto(
    id_carrossel: int,
    dados: CarouselUpdateRequest,
    usuario_logado=Depends(validar_token),
):
    _requer_admin(usuario_logado)
    try:
        return service.atualizar(id_carrossel, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/carrossel/{id_carrossel}")
def remover_foto(id_carrossel: int, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        service.remover(id_carrossel)
        return {"ok": True}
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))