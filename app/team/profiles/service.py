import shutil
from pathlib import Path
from team.profiles import model

PASTA_UPLOAD = Path(__file__).resolve().parent.parent.parent.parent / "upload"

def obter_perfil(id_usuario_logado):
    if id_usuario_logado is None:
        raise ValueError("Usuario não registrado")

    dados_usuario = model.get_usuario_logado(id_usuario_logado)

    if dados_usuario is None:
        raise ValueError("Perfil sem Dados")

    id_profissional, nome, bio, imagem_url = dados_usuario

    if nome is None and (bio is not None or imagem_url is not None):
        raise ValueError("Inconsistência: Nome ausente, com demais dados preenchidos")

    if nome is None:
        raise ValueError("Nome faltante")

    return {
        "id": id_profissional,
        "nome": nome,
        "bio": bio,
        "imagem_url": imagem_url,
    }


def post_perfil(id_usuario_logado, dados):
    id_profissional = model.post_perfil(id_usuario_logado, dados)

    return {
        "id": id_profissional,
        "nome": dados.nome,
        "bio": dados.bio,
        "imagem_url": dados.imagem_url,
    }


def update_perfil(id_usuario_logado, dados):
    dados_novos = dados.model_dump(exclude_none=True)

    if not dados_novos:
        raise ValueError("Nenhum dado enviado para atualização")

    nome_img = dados_novos.get("imagem_url")
    if nome_img:
        origem = PASTA_UPLOAD / "perfilpreview" / nome_img
        if origem.exists():
            (PASTA_UPLOAD / "perfil").mkdir(parents=True, exist_ok=True)
            shutil.move(str(origem), str(PASTA_UPLOAD / "perfil" / nome_img))

    model.update_perfil(id_usuario_logado, dados_novos)

    return obter_perfil(id_usuario_logado)