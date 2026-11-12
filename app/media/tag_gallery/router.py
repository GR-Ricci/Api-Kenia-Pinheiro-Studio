from fastapi import APIRouter, HTTPException, Depends
from auth import validar_token
from media.tag_gallery import service
from media.tag_gallery.schema import TagRequest, TagResponse

router = APIRouter(tags=["Tag"])


def _requer_admin(usuario_logado):
    if usuario_logado["tipo"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado.")


@router.post("/tags", response_model=TagResponse)
def criar_tag(dados: TagRequest, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        return service.criar_tag(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/tags", response_model=list[TagResponse])
def listar_tags(usuario_logado=Depends(validar_token)):
    return service.obter_tags()


@router.put("/tags/{id_tag}", response_model=TagResponse)
def renomear_tag(id_tag: int, dados: TagRequest, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        return service.renomear_tag(id_tag, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/tags/{id_tag}")
def remover_tag(id_tag: int, usuario_logado=Depends(validar_token)):
    _requer_admin(usuario_logado)
    try:
        service.remover_tag(id_tag)
        return {"ok": True}
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))