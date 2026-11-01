# contém as regras e decisões da funcionalidade.

"""
Exemplo de uso:
criar_galeria(dados)
listar_galeria()
"""

from profiles import model

def obter_perfil(id_usuario_logado):
    if id_usuario_logado is None:
        raise ValueError("Usuario não registrado")

    dados_usuario = model.get_usuario_logado(id_usuario_logado)

    if dados_usuario is None:
        raise ValueError("Perfil sem Dados")

    id_profissional, nome, bio, imagem_url = dados_usuario

    if nome is None and (bio is not None or imagem_url is not None):
        raise ValueError("Inconsistência: Nome ausente, com demais dados preenchidos")

    if nome is None:
        raise ValueError("Nome faltante")

    return{
        "id": id_profissional,
        "nome": nome,
        "bio": bio,
        "imagem_url": imagem_url
    }

def post_perfil(id_usuario_logado, dados):

    id_profissional = model.post_perfil(id_usuario_logado, dados)

    return{
        "id":id_profissional,
        "nome": dados.nome,
        "bio": dados.bio,
        "imagem_url": dados.imagem_url
    }

def update_perfil(id_usuario_logado, dados):

    # 1. Transforma o Pydantic em dicionário e remove os campos nulos
    dados_novos = dados.model_dump(exclude_none=True)

    # 2. Se o dicionário ficar vazio (o front não mandou nada), a gente barra
    if not dados_novos:
        raise ValueError("Nenhum dado enviado para atualização")


    model.update_perfil(id_usuario_logado, dados_novos) #não faz return, depois de atualizar tudo, usa o obter_perfil pra trazer tudo atualizado, coisas mdudadas e coisas antigas

    return obter_perfil(id_usuario_logado) #chama a def responsavel por trazer o usuario (agr ja esta atualizado pós commit, e traz o return pois vai ser return do return

