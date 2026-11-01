# contém as regras e decisões da funcionalidade.

"""
Exemplo de uso:
criar_galeria(dados)
listar_galeria()
"""

from gallery import model


def listar_tags():
    tags = []
    for id_tag, nome in model.listar_tags():
        tags.append({"id": id_tag, "nome": nome})
    return tags


def listar_galeria():
    #agrupa as tags dentro de cada foto, já na ordem de exibição
    fotos = {}
    for id_galeria, imagem_url, nome_tag in model.listar_galeria():
        if id_galeria not in fotos:
            fotos[id_galeria] = {
                "id": id_galeria,
                "imagem_url": imagem_url,
                "tags": []
            }

        if nome_tag is not None:                            #foto ainda sem tag
            fotos[id_galeria]["tags"].append(nome_tag)

    return list(fotos.values())
