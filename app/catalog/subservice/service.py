from catalog.subservice import model


def criar_subservico(dados):
    if model.verificar_subservico_existente(dados.nome, dados.id_servico):
        raise ValueError("Este subserviço já existe neste serviço.")

    info = model.obter_info_servico(dados.id_servico)
    if not info:
        raise ValueError("Serviço inválido.")

    id_sub = model.inserir_subservico(dados.nome, dados.id_servico)

    return {
        "id": id_sub,
        "nome": dados.nome,
        "id_servico": dados.id_servico,
        "ativo": True,
        "nome_servico": info[0],
        "nome_categoria": info[1],
    }


def obter_subservicos(id_servico=None):
    return model.listar_subservicos(id_servico)