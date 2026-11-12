from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from catalog.profissional_subservice import service, model
from catalog.profissional_subservice.schema import (
    ProfissionalSubservicoRequest,
    ProfissionalSubservicoUpdateRequest,
    ProfissionalSubservicoResponse,
)

router = APIRouter(tags=["ProfissionalSubservice"])


def _requer_profissional_ou_admin(usuario_logado):
    if usuario_logado["tipo"] not in ("ADMIN", "PROFISSIONAL"):
        raise HTTPException(status_code=403, detail="Acesso negado.")


def _resolve_id_prof(usuario_logado, id_prof_solicitado: int | None):
    """
    ADMIN: pode consultar qualquer id_profissional (se passar no body/URL).
    PROFISSIONAL: só pode o próprio.
    """
    if usuario_logado["tipo"] == "ADMIN":
        if id_prof_solicitado:
            return id_prof_solicitado

        # Admin sem id explícito: usa o próprio
        id_prof_proprio = model.obter_id_profissional_por_usuario(usuario_logado["id"])

        # Se não tiver perfil, cria um automaticamente em vez de dar erro
        if not id_prof_proprio:
            id_prof_proprio = model.criar_perfil_basico(usuario_logado["id"])

        return id_prof_proprio

    # PROFISSIONAL
    id_prof_logado = model.obter_id_profissional_por_usuario(usuario_logado["id"])
    if not id_prof_logado:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")

    if id_prof_solicitado and id_prof_solicitado != id_prof_logado:
        raise HTTPException(status_code=403, detail="Você só pode acessar seus próprios dados.")

    return id_prof_logado


@router.post("/profissional-subservicos", response_model=ProfissionalSubservicoResponse)
def vincular_subservico(
        dados: ProfissionalSubservicoRequest,
        usuario_logado=Depends(validar_token),
):
    _requer_profissional_ou_admin(usuario_logado)
    id_prof = _resolve_id_prof(usuario_logado, dados.id_profissional)
    try:
        return service.vincular(id_prof, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/profissional-subservicos", response_model=list[ProfissionalSubservicoResponse])
def listar_meus_subservicos(usuario_logado=Depends(validar_token)):
    _requer_profissional_ou_admin(usuario_logado)
    id_prof = _resolve_id_prof(usuario_logado, None)
    return service.listar_meus(id_prof)


@router.get(
    "/profissional-subservicos/{id_profissional}",
    response_model=list[ProfissionalSubservicoResponse],
)
def listar_de_profissional(
        id_profissional: int,
        usuario_logado=Depends(validar_token),
):
    _requer_profissional_ou_admin(usuario_logado)
    id_prof = _resolve_id_prof(usuario_logado, id_profissional)
    return service.listar_de_profissional(id_prof)


@router.put(
    "/profissional-subservicos/{id_profissional}/{id_subservico}",
    response_model=ProfissionalSubservicoResponse,
)
def atualizar_vinculo(
        id_profissional: int,
        id_subservico: int,
        dados: ProfissionalSubservicoUpdateRequest,
        usuario_logado=Depends(validar_token),
):
    _requer_profissional_ou_admin(usuario_logado)
    id_prof = _resolve_id_prof(usuario_logado, id_profissional)
    try:
        return service.atualizar_vinculo(id_prof, id_subservico, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/profissional-subservicos/{id_profissional}/{id_subservico}")
def remover_vinculo(
        id_profissional: int,
        id_subservico: int,
        usuario_logado=Depends(validar_token),
):
    _requer_profissional_ou_admin(usuario_logado)
    id_prof = _resolve_id_prof(usuario_logado, id_profissional)
    try:
        service.remover_vinculo(id_prof, id_subservico)
        return {"ok": True}
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))