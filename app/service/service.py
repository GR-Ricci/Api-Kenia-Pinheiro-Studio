# contém as regras e decisões da funcionalidade.

"""
Exemplo de uso:
criar_galeria(dados)
listar_galeria()
"""

from service import model


def listar_categorias():
    categorias = []
    for id_categoria, nome in model.listar_categorias():
        categorias.append({"id": id_categoria, "nome": nome})
    return categorias


def listar_servicos(id_categoria=None):
    servicos = []
    for id_servico, id_cat, nome, descricao, imagem_url in model.listar_servicos(id_categoria):
        servicos.append({
            "id": id_servico,
            "id_categoria": id_cat,
            "nome": nome,
            "descricao": descricao,
            "imagem_url": imagem_url
        })
    return servicos


def listar_profissionais_do_servico(id_servico):
    if model.buscar_servico(id_servico) is None:
        raise ValueError("Serviço não encontrado")

    #agrupa os subserviços dentro de cada profissional
    profissionais = {}
    for linha in model.listar_profissionais_do_servico(id_servico):

        #desempacotamento
        (id_profissional, nome, imagem_url,
         id_subservico, nome_subservico, preco, duracao_minutos, descricao, imagem_subservico) = linha

        if id_profissional not in profissionais:
            profissionais[id_profissional] = {
                "id": id_profissional,
                "nome": nome,
                "imagem_url": imagem_url,
                "subservicos": []
            }

        profissionais[id_profissional]["subservicos"].append({
            "id": id_subservico,
            "nome": nome_subservico,
            "preco": preco,
            "duracao_minutos": duracao_minutos,
            "descricao": descricao,
            "imagem_url": imagem_subservico
        })

    return list(profissionais.values())
