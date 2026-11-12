from catalog.category import model


def criar_categoria(dados):
    if model.verificar_categoria_existente(dados.nome):
        raise ValueError("Esta categoria já está cadastrada.")
    id_categoria = model.inserir_categoria(dados.nome)
    return {"id": id_categoria, "nome": dados.nome, "ativo": True}


def obter_categorias():
    return model.listar_categorias()


def atualizar(id_categoria, dados):
    atual = model.obter_categoria(id_categoria)
    if not atual:
        raise ValueError("Categoria não encontrada.")

    existente = model.buscar_por_nome(dados.nome)
    if existente and existente["id"] != id_categoria:
        raise ValueError("Já existe outra categoria com este nome.")

    model.atualizar_categoria(id_categoria, dados.nome, dados.ativo)
    return {"id": id_categoria, "nome": dados.nome, "ativo": dados.ativo}


def impacto_delete(id_categoria):
    if not model.obter_categoria(id_categoria):
        raise ValueError("Categoria não encontrada.")
    return model.contar_impacto_delete(id_categoria)


def remover(id_categoria, force=False):
    if not model.obter_categoria(id_categoria):
        raise ValueError("Categoria não encontrada.")

    impacto = model.contar_impacto_delete(id_categoria)
    tem_vinculo = impacto["vinculos_afetados"] > 0

    if tem_vinculo and not force:
        # Sinaliza que precisa confirmação — o router converte em 409
        raise ValueError(
            f"IMPACTO:{impacto['profissionais_afetadas']}:{impacto['vinculos_afetados']}"
        )

    if force:
        model.deletar_categoria_forcado(id_categoria)
    else:
        model.deletar_categoria(id_categoria)