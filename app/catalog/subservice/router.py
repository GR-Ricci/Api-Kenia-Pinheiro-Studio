from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from catalog.subservice import service
from catalog.subservice.schema import SubservicoRequest, SubservicoResponse

router = APIRouter(tags=["Subservice"])


@router.post("/subservicos", response_model=SubservicoResponse)
def criar_subservico(dados: SubservicoRequest, usuario_logado=Depends(validar_token)):
    try:
        return service.criar_subservico(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/subservicos", response_model=list[SubservicoResponse])
def listar_subservicos(
    id_servico: int | None = None,
    usuario_logado=Depends(validar_token),
):
    return service.obter_subservicos(id_servico)