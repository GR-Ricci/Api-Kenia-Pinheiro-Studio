# representa as tabelas e os dados usados no banco.


"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""

# fala com o banco: lê categorias, serviços e as profissionais de cada serviço.

from database import conect_database


def listar_categorias():
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM categoria
        WHERE ativo = TRUE
        ORDER BY ordem_exibicao NULLS LAST, nome
    """)
    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()
    return categorias


def listar_servicos(id_categoria):
    conexao = conect_database()
    cursor = conexao.cursor()

    sql = """
        SELECT s.id, s.id_categoria, s.nome, s.descricao, s.imagem_url
        FROM servico s
        JOIN categoria c ON c.id = s.id_categoria
        WHERE s.ativo = TRUE AND c.ativo = TRUE
    """
    parametros = []

    if id_categoria is not None:                    #filtro opcional por categoria
        sql += " AND s.id_categoria = %s"
        parametros.append(id_categoria)

    sql += " ORDER BY c.ordem_exibicao NULLS LAST, s.ordem_exibicao NULLS LAST, s.nome"

    cursor.execute(sql, parametros)
    servicos = cursor.fetchall()

    cursor.close()
    conexao.close()
    return servicos


def buscar_servico(id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT s.id, s.nome
        FROM servico s
        JOIN categoria c ON c.id = s.id_categoria
        WHERE s.id = %s AND s.ativo = TRUE AND c.ativo = TRUE
    """, (id_servico,))
    servico = cursor.fetchone()

    cursor.close()
    conexao.close()
    return servico


def listar_profissionais_do_servico(id_servico):
    # uma linha por (profissional, subserviço), com o preço e a duração dessa profissional
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT p.id, p.nome, p.imagem_url,
               sub.id, sub.nome, ps.preco, ps.duracao_minutos, ps.descricao, ps.imagem_url
        FROM profissional_subservico ps
        JOIN subservico sub ON sub.id = ps.id_subservico
        JOIN profissional p ON p.id = ps.id_profissional
        WHERE sub.id_servico = %s
          AND ps.ativo = TRUE AND sub.ativo = TRUE AND p.ativo = TRUE
        ORDER BY p.ordem_exibicao NULLS LAST, p.nome, ps.ordem_exibicao NULLS LAST, sub.nome
    """, (id_servico,))
    linhas = cursor.fetchall()

    cursor.close()
    conexao.close()
    return linhas
