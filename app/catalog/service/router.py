from fastapi import APIRouter, HTTPException, Depends, Query
from auth import validar_token
from catalog.service import service
from catalog.service.schema import (
    ServiceRequest,
    ServiceUpdateRequest,
    ServiceResponse,
    ServiceDeleteCheckResponse,
)

router = APIRouter(tags=["Service"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.post("/servicos", response_model=ServiceResponse)
def criar_servico(dados: ServiceRequest, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        return service.criar_servico(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/servicos", response_model=list[ServiceResponse])
def listar_servicos(
    id_categoria: int | None = None,
    usuario_logado=Depends(validar_token),
):
    return service.obter_servicos(id_categoria)


@router.put("/servicos/{id_servico}", response_model=ServiceResponse)
def atualizar_servico(
    id_servico: int,
    dados: ServiceUpdateRequest,
    usuario_logado=Depends(validar_token),
):
    _requer_admin(usuario_logado)
    try:
        return service.atualizar(id_servico, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/servicos/{id_servico}/impacto-delete", response_model=ServiceDeleteCheckResponse)
def impacto_delete(id_servico: int, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        impacto = service.impacto_delete(id_servico)
        return {
            "pode_deletar": impacto["vinculos_afetados"] == 0,
            "profissionais_afetadas": impacto["profissionais_afetadas"],
            "subservicos_afetados": impacto["subservicos_afetados"],
        }
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.delete("/servicos/{id_servico}")
def remover_servico(
    id_servico: int,
    force: bool = Query(False),
    usuario_logado=Depends(validar_token),
):
    _requer_admin(usuario_logado)
    try:
        service.remover(id_servico, force=force)
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