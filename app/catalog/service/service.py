import shutil
from pathlib import Path
from catalog.service import model

PASTA_UPLOAD = Path(__file__).resolve().parent.parent.parent.parent / "upload"
PASTA_PREVIEW = PASTA_UPLOAD / "servicopreview"
PASTA_SERVICO = PASTA_UPLOAD / "servico"


def criar_servico(dados):
    if model.verificar_servico_existente(dados.nome, dados.id_categoria):
        raise ValueError("Este serviço já está cadastrado nesta categoria.")

    if dados.imagem_url:
        origem = PASTA_PREVIEW / dados.imagem_url
        destino = PASTA_SERVICO / dados.imagem_url

        # Se a imagem está no preview, move para a pasta final
        if origem.is_file():
            PASTA_SERVICO.mkdir(parents=True, exist_ok=True)
            shutil.move(str(origem), str(destino))
        # Se não está no preview E não está na pasta final, aí sim dá erro
        elif not destino.is_file():
            raise ValueError(f"Imagem '{dados.imagem_url}' não encontrada nas pastas de upload.")

    id_servico = model.inserir_servico(dados.nome, dados.id_categoria, dados.imagem_url)
    nome_categoria = model.obter_nome_categoria(dados.id_categoria)

    return {
        "id": id_servico,
        "nome": dados.nome,
        "id_categoria": dados.id_categoria,
        "imagem_url": dados.imagem_url,
        "ativo": True,
        "nome_categoria": nome_categoria,
    }


def obter_servicos(id_categoria=None):
    return model.listar_servicos(id_categoria)


def atualizar(id_servico, dados):
    atual = model.obter_servico(id_servico)
    if not atual:
        raise ValueError("Serviço não encontrado.")

    nome_categoria = model.obter_nome_categoria(dados.id_categoria)
    if not nome_categoria:
        raise ValueError("Categoria inválida.")

    if model.verificar_servico_existente(dados.nome, dados.id_categoria, ignorar_id=id_servico):
        raise ValueError("Já existe um serviço com este nome nesta categoria.")

    # Se veio imagem nova, tenta mover (mas não quebra se já estiver no lugar certo)
    if dados.imagem_url and dados.imagem_url != atual["imagem_url"]:
        origem = PASTA_PREVIEW / dados.imagem_url
        destino = PASTA_SERVICO / dados.imagem_url

        if origem.is_file():
            PASTA_SERVICO.mkdir(parents=True, exist_ok=True)
            shutil.move(str(origem), str(destino))
        elif not destino.is_file():
            raise ValueError(f"Imagem '{dados.imagem_url}' não encontrada nas pastas de upload.")

    model.atualizar_servico(
        id_servico, dados.nome, dados.id_categoria, dados.imagem_url, dados.ativo
    )

    return {
        "id": id_servico,
        "nome": dados.nome,
        "id_categoria": dados.id_categoria,
        "imagem_url": dados.imagem_url,
        "ativo": dados.ativo,
        "nome_categoria": nome_categoria,
    }


def impacto_delete(id_servico):
    if not model.obter_servico(id_servico):
        raise ValueError("Serviço não encontrado.")
    return model.contar_impacto_delete(id_servico)


def remover(id_servico, force=False):
    if not model.obter_servico(id_servico):
        raise ValueError("Serviço não encontrado.")

    impacto = model.contar_impacto_delete(id_servico)
    if impacto["vinculos_afetados"] > 0 and not force:
        raise ValueError(
            f"IMPACTO:{impacto['profissionais_afetadas']}:{impacto['vinculos_afetados']}"
        )

    if force:
        model.deletar_servico_forcado(id_servico)
    else:
        model.deletar_servico(id_servico)