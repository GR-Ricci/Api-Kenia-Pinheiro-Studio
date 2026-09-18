# contém as regras e decisões da funcionalidade.

"""
Exemplo de uso:
criar_galeria(dados)
listar_galeria()
"""
# contém as regras e decisões do convite.

from invite import model
import secrets
from datetime import datetime, timedelta, timezone
import bcrypt


def gerar_convite(tipo):
    if tipo not in ("ADMIN", "PROFISSIONAL"):
        raise ValueError("Tipo inválido")

    token = secrets.token_urlsafe(32)

    expira_em = datetime.now(timezone.utc) + timedelta(hours=24)

    model.criar_convite(token,tipo,expira_em)

    return{
    "token": token,
    "link": f"/cadastro?token={token}",
    "expira_em": expira_em
    }


def validar_token(token):

    convite = model.buscar_convite(token)

    if convite is None:
        return {"valido": False, "tipo": "", "mensagem": "Convite não encontrado"}

    #desempacotamento
    _, tipo, expira_em, usado = convite

    if tipo not in ("ADMIN", "PROFISSIONAL") :                                  #mensagem de invalido, não gerar erro
        return {"valido": False, "tipo": "", "mensagem": "Convite invalido"}    #pois apenas avisa o usuario e n quebra

    if expira_em < datetime.now(timezone.utc):
        return {"valido": False, "tipo": "", "mensagem": "Convite expirado"}

    if usado:
        return {"valido": False, "tipo": "", "mensagem": "Convite já usado"}

    return {"valido": True,  "tipo": tipo, "mensagem": "Convite encontrado valido"}



def permitir_cadastro(token, senha):

    convite = validar_token(token)

    if convite["valido"] == False:
        raise ValueError(convite["mensagem"])           #gera erro, não deveria ter ninguem ali, tem q fechar abrupto

    if len(senha) < 8:
        raise ValueError("Senha muito curta")
    if len(senha) > 16:
        raise ValueError("Senha muito grande")

    if not any(c.isupper() for c in senha):
        raise ValueError("Precisa ter uma letra maiúscula")

    if not any(c.isdigit() for c in senha):
        raise ValueError("Precisa ter um número")

    for i in range(len(senha) - 2):
        if senha[i] == senha[i + 1] == senha[i + 2]:
            raise ValueError("Não pode repetir 3 caracteres seguidos")


def criptografar_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def cadastro(token, senha, email):
    permitir_cadastro(token, senha)
    senha_hash = criptografar_senha(senha)

    #desempacotamento
    id_convite, tipo, _, _ = model.buscar_convite(token)

    model.criar_usuario(email, senha_hash, tipo)
    model.usar_convite(id_convite)
    return{"email": email, "tipo": tipo}