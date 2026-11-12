from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from informative.about import service
from informative.about.schema import ContatoUpdate, ContatoResponse

router = APIRouter(tags=["Contact"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.get("/contato", response_model=ContatoResponse)
def obter_contato():
    """Rota PÚBLICA — a página de contato precisa mostrar sem login."""
    return service.obter()


@router.put("/contato", response_model=ContatoResponse)
def atualizar_contato(dados: ContatoUpdate, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    return service.atualizar(dados)