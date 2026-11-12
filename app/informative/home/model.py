from pathlib import Path

from database import conect_database

PASTA_HOME = Path(__file__).resolve().parents[3] / "upload" / "home"


def obter_id_admin():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM usuario WHERE tipo = 'ADMIN' ORDER BY id LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    conexao.close()
    return row[0] if row else None


def obter_home_atual():
    if not PASTA_HOME.exists():
        return {"imagem_url": None, "atualizado_em": None}

    # Só existe 1 arquivo por vez (o upload apaga o antigo)
    for arquivo in PASTA_HOME.iterdir():
        if arquivo.is_file():
            return {
                "imagem_url": arquivo.name,
                "atualizado_em": int(arquivo.stat().st_mtime),
            }
    return {"imagem_url": None, "atualizado_em": None}


def deletar_home():
    if not PASTA_HOME.exists():
        return False
    for arquivo in PASTA_HOME.iterdir():
        if arquivo.is_file():
            arquivo.unlink()
    return True