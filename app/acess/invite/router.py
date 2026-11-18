from fastapi import APIRouter, HTTPException, Depends

from acess.invite.schema import ConviteRequest, CadastroRequest, ConviteResponse, CadastroResponse
from acess.invite import service
from auth import validar_token


router = APIRouter(tags=["Invite"])


@router.post("/invites", response_model=ConviteResponse)
def criar_convite(dados: ConviteRequest, usuario_logado=Depends(validar_token)):
    # ← MUDOU: agora exige superadmin
    if usuario_logado["tipo"] != "ADMIN" or not usuario_logado.get("superadmin"):
        raise HTTPException(status_code=403, detail="Apenas superadmin pode gerar convites.")

    try:
        return service.gerar_convite(dados.tipo)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/invites/{token}")
def validar_convite(token: str):
    return service.validar_token(token)


@router.post("/cadastro", response_model=CadastroResponse)
def cadastrar(dados: CadastroRequest):
    try:
        return service.cadastro(dados.token, dados.senha, dados.email)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))