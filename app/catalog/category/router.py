from fastapi import APIRouter, HTTPException, Depends, Query
from auth import validar_token
from catalog.category import service
from catalog.category.schema import (
    CategoryRequest,
    CategoryUpdateRequest,
    CategoryResponse,
    CategoryDeleteCheckResponse,
)

router = APIRouter(tags=["Category"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.post("/categorias", response_model=CategoryResponse)
def criar_categoria(dados: CategoryRequest, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        return service.criar_categoria(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/categorias", response_model=list[CategoryResponse])
def listar_todas_categorias(usuario_logado=Depends(validar_token)):
    return service.obter_categorias()


@router.put("/categorias/{id_categoria}", response_model=CategoryResponse)
def atualizar_categoria(
    id_categoria: int,
    dados: CategoryUpdateRequest,
    usuario_logado=Depends(validar_token),
):
    _requer_admin(usuario_logado)
    try:
        return service.atualizar(id_categoria, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get(
    "/categorias/{id_categoria}/impacto-delete",
    response_model=CategoryDeleteCheckResponse,
)
def impacto_delete(id_categoria: int, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        impacto = service.impacto_delete(id_categoria)
        return {
            "pode_deletar": impacto["vinculos_afetados"] == 0,
            "profissionais_afetadas": impacto["profissionais_afetadas"],
            "servicos_afetados": impacto["servicos_afetados"],
            "subservicos_afetados": impacto["subservicos_afetados"],
        }
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.delete("/categorias/{id_categoria}")
def remover_categoria(
    id_categoria: int,
    force: bool = Query(False),
    usuario_logado=Depends(validar_token),
):
    _requer_admin(usuario_logado)
    try:
        service.remover(id_categoria, force=force)
        return {"ok": True}
    except ValueError as erro:
        msg = str(erro)
        if msg.startswith("IMPACTO:"):
            _, profs, vincs = msg.split(":")
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "TEM_VINCULO",
                    "profissionais_afetadas": int(profs),
                    "vinculos_afetados": int(vincs),
                    "mensagem": f"{profs} profissional(is) oferecem serviços desta categoria.",
                },
            )
        raise HTTPException(status_code=400, detail=msg)