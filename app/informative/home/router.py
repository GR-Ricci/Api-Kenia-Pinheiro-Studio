from fastapi import APIRouter, HTTPException, Depends

from auth import validar_token
from informative.home import model
from informative.home.schema import HomeResponse

router = APIRouter(tags=["Home"])


@router.get("/home", response_model=HomeResponse)
def obter_home():
    """Público — retorna a imagem atual da home."""
    return model.obter_home_atual()


@router.delete("/home")
def deletar_home(usuario_logado=Depends(validar_token)):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")
    model.deletar_home()
    return {"ok": True}