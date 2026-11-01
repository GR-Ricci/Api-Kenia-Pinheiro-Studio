# representa as tabelas e os dados usados no banco.


"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""

# fala com o banco: lê as fotos da galeria e as tags usadas no filtro.

from database import conect_database


def listar_tags():
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM tag
        ORDER BY nome
    """)
    tags = cursor.fetchall()

    cursor.close()
    conexao.close()
    return tags


def listar_galeria():
    # uma linha por (foto, tag): a mesma foto pode estar em mais de uma tag
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT g.id, g.imagem_url, t.nome
        FROM galeria g
        LEFT JOIN galeria_tag gt ON gt.id_galeria = g.id
        LEFT JOIN tag t ON t.id = gt.id_tag
        ORDER BY g.ordem_exibicao NULLS LAST, g.id, t.nome
    """)
    linhas = cursor.fetchall()

    cursor.close()
    conexao.close()
    return linhas
