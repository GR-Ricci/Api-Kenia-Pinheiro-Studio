from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from informative.hours import service
from informative.hours.schema import FuncionamentoDiaUpdate, FuncionamentoDiaResponse

router = APIRouter(tags=["Funcionamento"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.get("/funcionamento", response_model=list[FuncionamentoDiaResponse])
def obter_funcionamento():
    """Público — página de horários precisa mostrar sem login."""
    return service.obter()


@router.put("/funcionamento/{dia}", response_model=FuncionamentoDiaResponse)
def atualizar_dia(dia: int, dados: FuncionamentoDiaUpdate, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        return service.atualizar_dia(dia, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))