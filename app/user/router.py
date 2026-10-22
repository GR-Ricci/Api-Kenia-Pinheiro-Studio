# define as rotas, recebe as requisições e chama os services.

"""
Exemplo de uso:
GET /galeria
POST /galeria
"""

from fastapi import APIRouter, HTTPException, Depends

from user.schema import LoginRequest, LoginResponse
from user import service
from auth import validar_token

router = APIRouter(tags=["User"])

@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest):
    try:
        return service.verificar_login(dados.email, dados.senha)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))



@router.get("/teste") # Rota de teste (cobaia)
def testar_login(usuario_logado = Depends(validar_token)):
    # Se chegou aqui, o Porteiro deixou passar!
    return {
        "mensagem": "Você está autenticado!",
        "dados_do_token": usuario_logado # Vai mostrar o id e o tipo que estavam no token
    }
