# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""


from fastapi import APIRouter

from user.schema import UsuarioEmailResponse
from user.service import obter_emails

router = APIRouter(tags=["User"])


@router.get("/usuarios/emails", response_model=list[UsuarioEmailResponse])
def listar_emails_usuario():
    return obter_emails()

