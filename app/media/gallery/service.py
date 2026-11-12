from media.gallery import model
from media.tag_gallery import model as tag_model


def criar_foto(dados):
    # Valida que todas as tags existem
    for id_tag in dados.id_tags:
        if not tag_model.obter_tag(id_tag):
            raise ValueError(f"Tag {id_tag} não encontrada.")

    id_galeria = model.inserir_galeria(dados.imagem_url)

    for id_tag in dados.id_tags:
        model.inserir_galeria_tag(id_galeria, id_tag)

    return _montar_resposta(id_galeria)


def listar_fotos():
    return model.listar_galerias()


def atualizar_foto(id_galeria, dados):
    if not model.obter_galeria(id_galeria):
        raise ValueError("Foto não encontrada.")

    if dados.imagem_url is not None:
        model.atualizar_imagem(id_galeria, dados.imagem_url)

    if dados.id_tags is not None:
        for id_tag in dados.id_tags:
            if not tag_model.obter_tag(id_tag):
                raise ValueError(f"Tag {id_tag} não encontrada.")
        model.deletar_galeria_tags(id_galeria)
        for id_tag in dados.id_tags:
            model.inserir_galeria_tag(id_galeria, id_tag)

    return _montar_resposta(id_galeria)


def remover_foto(id_galeria):
    if not model.obter_galeria(id_galeria):
        raise ValueError("Foto não encontrada.")
    model.deletar_galeria(id_galeria)


def _montar_resposta(id_galeria):
    # Busca a foto atualizada e monta com tags
    todas = model.listar_galerias()
    for foto in todas:
        if foto["id"] == id_galeria:
            return foto
    raise ValueError("Foto não encontrada após salvar.")