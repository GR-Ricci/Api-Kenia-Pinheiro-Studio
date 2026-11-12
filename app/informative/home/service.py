from media.carousel import model


def criar(dados):
    if not model.verificar_categoria_existe(dados.id_categoria):
        raise ValueError("Categoria inválida.")

    id_carrossel = model.inserir_carrossel(
        dados.imagem_url, dados.id_categoria, dados.ordem_exibicao
    )
    nome_categoria = model.obter_nome_categoria(dados.id_categoria)

    return {
        "id": id_carrossel,
        "imagem_url": dados.imagem_url,
        "id_categoria": dados.id_categoria,
        "nome_categoria": nome_categoria,
        "ordem_exibicao": dados.ordem_exibicao,
    }


def listar():
    return model.listar_carrosseis()


def atualizar(id_carrossel, dados):
    atual = model.obter_carrossel(id_carrossel)
    if not atual:
        raise ValueError("Foto não encontrada.")

    nova_categoria = (
        dados.id_categoria if dados.id_categoria is not None else atual["id_categoria"]
    )
    nova_ordem = (
        dados.ordem_exibicao
        if dados.ordem_exibicao is not None
        else atual["ordem_exibicao"]
    )

    if not model.verificar_categoria_existe(nova_categoria):
        raise ValueError("Categoria inválida.")

    model.atualizar_carrossel(id_carrossel, nova_categoria, nova_ordem)
    nome_categoria = model.obter_nome_categoria(nova_categoria)

    return {
        "id": id_carrossel,
        "imagem_url": atual["imagem_url"],
        "id_categoria": nova_categoria,
        "nome_categoria": nome_categoria,
        "ordem_exibicao": nova_ordem,
    }


def remover(id_carrossel):
    if not model.obter_carrossel(id_carrossel):
        raise ValueError("Foto não encontrada.")
    model.deletar_carrossel(id_carrossel)