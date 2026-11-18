from catalog.profissional_subservice import model
from catalog.package import model as pacote_model


def vincular(id_profissional, dados):
    if model.verificar_vinculo_existente(id_profissional, dados.id_subservico):
        raise ValueError("Você já oferece este subserviço.")

    info = model.obter_info_subservico(dados.id_subservico)
    if not info:
        raise ValueError("Subserviço inválido.")

    model.inserir_vinculo(
        id_profissional,
        dados.id_subservico,
        dados.imagem_url,
        dados.preco,
        dados.duracao_minutos,
        dados.descricao,
    )

    return {
        "id_profissional": id_profissional,
        "id_subservico": dados.id_subservico,
        "nome_subservico": info[0],
        "nome_servico": info[1],
        "nome_categoria": info[2],
        "imagem_url": dados.imagem_url,
        "preco": dados.preco,
        "duracao_minutos": dados.duracao_minutos,
        "ativo": True,
        "descricao": dados.descricao,
    }


def listar_meus(id_profissional):
    return model.listar_por_profissional(id_profissional)


def listar_de_profissional(id_profissional):
    return model.listar_por_profissional(id_profissional)


def atualizar_vinculo(id_profissional, id_subservico, dados):
    atual = model.obter_vinculo(id_profissional, id_subservico)
    if not atual:
        raise ValueError("Vínculo não encontrado.")

    novo_preco = dados.preco if dados.preco is not None else atual["preco"]
    nova_duracao = dados.duracao_minutos if dados.duracao_minutos is not None else atual["duracao_minutos"]
    novo_ativo = dados.ativo if dados.ativo is not None else atual["ativo"]
    nova_imagem = dados.imagem_url if dados.imagem_url is not None else atual["imagem_url"]
    nova_descricao = dados.descricao if dados.descricao is not None else atual["descricao"]

    model.atualizar_vinculo(
        id_profissional, id_subservico, nova_imagem, novo_preco, nova_duracao, novo_ativo, nova_descricao
    )

    info = model.obter_info_subservico(id_subservico)
    return {
        "id_profissional": id_profissional,
        "id_subservico": id_subservico,
        "nome_subservico": info[0],
        "nome_servico": info[1],
        "nome_categoria": info[2],
        "imagem_url": nova_imagem,
        "preco": novo_preco,
        "duracao_minutos": nova_duracao,
        "ativo": novo_ativo,
        "descricao": nova_descricao,
    }


def remover_vinculo(id_profissional, id_subservico):
    if not model.obter_vinculo(id_profissional, id_subservico):
        raise ValueError("Vínculo não encontrado.")

    qtd_pacotes = pacote_model.contar_pacotes_usando_vinculo(id_profissional, id_subservico)
    if qtd_pacotes > 0:
        raise ValueError(
            f"Este subserviço está em {qtd_pacotes} pacote(s). "
            "Remova-o dos pacotes antes de desvincular."
        )

    model.deletar_vinculo(id_profissional, id_subservico)