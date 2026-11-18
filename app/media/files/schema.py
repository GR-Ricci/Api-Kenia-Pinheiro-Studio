from pydantic import BaseModel


class UploadResponse(BaseModel):
    imagem_url: str