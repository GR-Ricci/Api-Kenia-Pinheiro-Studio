from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from auth import validar_token
from media.files import service
from media.files.schema import UploadResponse

router = APIRouter(tags=["Upload"])


@router.post("/upload/{category}", response_model=UploadResponse)
def upload_arquivo(
    category: str,
    arquivo: UploadFile = File(...),
    usuario_logado=Depends(validar_token),
):
    try:
        nome = service.salvar_arquivo(arquivo, category, usuario_logado["id"])
        return {"imagem_url": nome}
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/upload/{category}/{filename}")
def deletar_arquivo(
    category: str,
    filename: str,
    usuario_logado=Depends(validar_token),
):
    try:
        return service.deletar_arquivo(category, filename)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))