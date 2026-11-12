from informative.about import model


def obter():
    model.garantir_linha()
    return model.obter_contato()


def atualizar(dados):
    model.garantir_linha()
    atual = model.obter_contato()
    model.atualizar_contato(atual["id"], dados)
    return model.obter_contato()