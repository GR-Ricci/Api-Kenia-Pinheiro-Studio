from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from team.staff import service
from team.staff.schema import StaffResponse, StaffStatusRequest

router = APIRouter(tags=["Staff"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.get("/staff/me", response_model=StaffResponse)
def obter_meu_staff(usuario_logado=Depends(validar_token)):
    """Retorna os dados do usuário logado (útil pra profissional saber seu id_profissional)."""
    try:
        return service.obter_meu(usuario_logado["id"])
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.get("/staff", response_model=list[StaffResponse])
def listar_staff(usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    return service.listar_todos()


@router.patch("/staff/{id_usuario}/status")
def alterar_status(
    id_usuario: int,
    dados: StaffStatusRequest,
    usuario_logado=Depends(validar_token),
):
    _requer_admin(usuario_logado)
    if id_usuario == usuario_logado["id"]:
        raise HTTPException(status_code=400, detail="Você não pode alterar seu próprio status.")
    try:
        return service.alterar_status(id_usuario, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/staff/{id_usuario}")
def remover_staff(id_usuario: int, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    if id_usuario == usuario_logado["id"]:
        raise HTTPException(status_code=400, detail="Você não pode excluir a si mesmo.")
    try:
        return service.remover(id_usuario)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))