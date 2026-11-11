from media.tag_gallery import model


def criar_tag(dados):
    if model.verificar_tag_existente(dados.nome):
        raise ValueError("Esta tag já existe.")

    id_tag = model.inserir_tag(dados.nome)
    return {"id": id_tag, "nome": dados.nome}


def obter_tags():
    return model.listar_tags()


def renomear_tag(id_tag, dados):
    if not model.obter_tag(id_tag):
        raise ValueError("Tag não encontrada.")

    # Se o novo nome já existe em outra tag, bloqueia
    conexao_check = model.verificar_tag_existente(dados.nome)
    if conexao_check:
        atual = model.obter_tag(id_tag)
        if atual["nome"].lower() != dados.nome.lower():
            raise ValueError("Já existe outra tag com este nome.")

    model.atualizar_tag(id_tag, dados.nome)
    return {"id": id_tag, "nome": dados.nome}


def remover_tag(id_tag):
    if not model.obter_tag(id_tag):
        raise ValueError("Tag não encontrada.")
    model.deletar_tag(id_tag)