from acess.user import model
import bcrypt

import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


def gerar_token(id_usuario, tipo, superadmin):
    tempo_expiracao = datetime.now(timezone.utc) + timedelta(days=7)

    payload = {
        "id": id_usuario,
        "tipo": tipo,
        "superadmin": superadmin,      # ← NOVO
        "exp": tempo_expiracao,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verificar_login(email, senha):
    dados_usuario = model.dados_login(email)

    if dados_usuario is None:
        raise ValueError("E-mail ou senha incorretos")

    id_usuario, senha_hash, tipo, ativo, superadmin = dados_usuario   # ← +superadmin

    senha_valida = bcrypt.checkpw(senha.encode(), senha_hash.encode())

    if not senha_valida:
        raise ValueError("E-mail ou senha incorretos")

    if not ativo:
        raise ValueError("Usuário não vinculado")

    token_jwt = gerar_token(id_usuario, tipo, superadmin)

    return {
        "access_token": token_jwt,
        "tipo": tipo,
        "superadmin": superadmin,      # ← NOVO (útil pro front saber)
        "id": id_usuario,
    }