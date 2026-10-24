# contém as regras e decisões da funcionalidade.

"""
Exemplo de uso:
criar_galeria(dados)
listar_galeria()
"""

from employee import model


def listar_cards():
    profissionais = model.listar_profissionais()
    categorias = model.listar_categorias_dos_profissionais()
    jornadas = model.listar_jornadas()

    #um card por profissional, já na ordem de exibição
    cards = {}
    for id_profissional, nome, bio, imagem_url in profissionais:
        cards[id_profissional] = {
            "id": id_profissional,
            "nome": nome,
            "bio": bio,
            "imagem_url": imagem_url,
            "categorias": [],
            "jornada": []
        }

    #desempacotamento
    for id_profissional, nome_categoria, _ in categorias:
        if id_profissional in cards:                        #ignora profissional inativo
            cards[id_profissional]["categorias"].append(nome_categoria)

    for id_profissional, dia_semana, hora_inicio, hora_fim in jornadas:
        if id_profissional in cards:
            cards[id_profissional]["jornada"].append({
                "dia_semana": dia_semana,
                "hora_inicio": hora_inicio,
                "hora_fim": hora_fim
            })

    return list(cards.values())
