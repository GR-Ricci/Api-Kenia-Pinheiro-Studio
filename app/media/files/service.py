import uuid
from pathlib import Path

PASTA_UPLOAD = Path(__file__).resolve().parent.parent.parent.parent / "upload"

def salvar_arquivo(arquivo, category, id_usuario):
    extensao = Path(arquivo.filename).suffix

    if category == "perfil":
        nome = f"{id_usuario}{extensao}"
        pasta_destino = PASTA_UPLOAD / "perfilpreview"
    elif category == "servico":
        nome = f"{uuid.uuid4().hex}{extensao}"
        pasta_destino = PASTA_UPLOAD / "servicopreview"
    elif category == "profissional_subservico":
        nome = f"{uuid.uuid4().hex}{extensao}"
        pasta_destino = PASTA_UPLOAD / "profissional_subservico"
    elif category == "galeria":
        nome = f"{uuid.uuid4().hex}{extensao}"
        pasta_destino = PASTA_UPLOAD / "galeria"
    elif category == "carrossel":
        nome = f"{uuid.uuid4().hex}{extensao}"
        pasta_destino = PASTA_UPLOAD / "carrossel"
    elif category == "pacote":
        nome = f"{uuid.uuid4().hex}{extensao}"
        pasta_destino = PASTA_UPLOAD / "pacotepreview"
    elif category == "home":
        nome = f"{id_usuario}{extensao}"
        pasta_destino = PASTA_UPLOAD / "home"
        if pasta_destino.exists():
            for antigo in pasta_destino.glob(f"{id_usuario}.*"):
                antigo.unlink()
    else:
        raise ValueError("Categoria inválida")

    pasta_destino.mkdir(parents=True, exist_ok=True)
    caminho = pasta_destino / nome

    with open(caminho, "wb") as f:
        f.write(arquivo.file.read())

    return nome


def deletar_arquivo(category, filename):
    if category == "perfil":
        pasta_destino = PASTA_UPLOAD / f"{category}preview"
    else:
        raise ValueError("Categoria Invalida")

    caminho = pasta_destino / filename

    if caminho.exists():
        caminho.unlink()

    return True