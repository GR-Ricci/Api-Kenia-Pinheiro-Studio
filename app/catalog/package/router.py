from fastapi import APIRouter, HTTPException, Depends, Query

from auth import validar_token
from catalog.package import model, service
from catalog.package.schema import (
    PacoteRequest,
    PacoteResponse,
    PacoteDeleteCheckResponse,
    SubservicoRapidoRequest,
    SubservicoRapidoResponse,
)

router = APIRouter(tags=["Package"])


def _requer_profissional_ou_admin(usuario_logado):
    if usuario_logado["tipo"] not in ("ADMIN", "PROFISSIONAL"):
        raise HTTPException(status_code=403, detail="Acesso negado.")


def _id_profissional_logado(usuario_logado):
    id_prof = model.obter_id_profissional_por_usuario(usuario_logado["id"])
    if not id_prof:
        raise HTTPException(
            status_code=404,
            detail="Usuário sem perfil profissional. Cadastre o perfil antes.",
        )
    return id_prof


# ===================== ROTAS FIXAS (antes das dinâmicas) =====================

@router.post("/pacotes", response_model=PacoteResponse)
def criar_pacote(dados: PacoteRequest, usuario_logado=Depends(validar_token)):
    _requer_profissional_ou_admin(usuario_logado)
    try:
        return service.criar(usuario_logado, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/pacotes", response_model=list[PacoteResponse])
def listar_pacotes(usuario_logado=Depends(validar_token)):
    _requer_profissional_ou_admin(usuario_logado)
    if usuario_logado["tipo"] == "ADMIN":
        return service.listar_todos()
    id_prof = _id_profissional_logado(usuario_logado)
    return service.listar_do_profissional(id_prof)


@router.post("/pacotes/subservico-rapido", response_model=SubservicoRapidoResponse)
def criar_subservico_rapido(
    dados: SubservicoRapidoRequest,
    usuario_logado=Depends(validar_token),
):
    _requer_profissional_ou_admin(usuario_logado)
    try:
        id_prof = _id_profissional_logado(usuario_logado)
        return service.criar_subservico_rapido(id_prof, dados.nome)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


# ===================== ROTAS DINÂMICAS =====================

@router.get("/pacotes/{id_pacote}", response_model=PacoteResponse)
def obter_pacote(id_pacote: int, usuario_logado=Depends(validar_token)):
    _requer_profissional_ou_admin(usuario_logado)
    try:
        return service.obter(id_pacote, usuario_logado)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.put("/pacotes/{id_pacote}", response_model=PacoteResponse)
def atualizar_pacote(
    id_pacote: int,
    dados: PacoteRequest,
    usuario_logado=Depends(validar_token),
):
    _requer_profissional_ou_admin(usuario_logado)
    try:
        return service.atualizar(id_pacote, usuario_logado, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get(
    "/pacotes/{id_pacote}/impacto-delete",
    response_model=PacoteDeleteCheckResponse,
)
def impacto_delete(id_pacote: int, usuario_logado=Depends(validar_token)):
    _requer_profissional_ou_admin(usuario_logado)
    try:
        impacto = service.impacto_delete(id_pacote, usuario_logado)
        return {
            "pode_deletar": impacto["agendamentos"] == 0,
            "itens": impacto["itens"],
            "agendamentos_afetados": impacto["agendamentos"],
        }
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.delete("/pacotes/{id_pacote}")
def remover_pacote(
    id_pacote: int,
    force: bool = Query(False),
    usuario_logado=Depends(validar_token),
):
    _requer_profissional_ou_admin(usuario_logado)
    try:
        service.remover(id_pacote, usuario_logado, force=force)
        return {"ok": True}
    except ValueError as erro:
        msg = str(erro)
        if msg.startswith("IMPACTO:"):
            qtd = int(msg.split(":")[1])
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "TEM_AGENDAMENTO",
                    "agendamentos_afetados": qtd,
                    "mensagem": f"{qtd} agendamento(s) usam este pacote.",
                },
            )
        raise HTTPException(status_code=400, detail=msg)