# representa as tabelas e os dados usados no banco.


"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""

# fala com o banco: lê os dados usados nos cards dos funcionários.

from database import conect_database


def listar_profissionais():
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, bio, imagem_url
        FROM profissional
        WHERE ativo = TRUE
        ORDER BY ordem_exibicao NULLS LAST, nome
    """)
    profissionais = cursor.fetchall()

    cursor.close()
    conexao.close()
    return profissionais


def listar_categorias_dos_profissionais():
    # categorias dos serviços que cada profissional atende (ex: Cabelos, Unhas)
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT DISTINCT ps.id_profissional, c.nome, c.ordem_exibicao
        FROM profissional_subservico ps
        JOIN subservico sub ON sub.id = ps.id_subservico
        JOIN servico s ON s.id = sub.id_servico
        JOIN categoria c ON c.id = s.id_categoria
        WHERE ps.ativo = TRUE AND sub.ativo = TRUE AND s.ativo = TRUE AND c.ativo = TRUE
        ORDER BY ps.id_profissional, c.ordem_exibicao NULLS LAST, c.nome
    """)
    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()
    return categorias


def listar_jornadas():
    # só os dias em que a profissional trabalha (horário preenchido)
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_profissional, dia_semana, hora_inicio, hora_fim
        FROM jornada
        WHERE ativo = TRUE AND hora_inicio IS NOT NULL
        ORDER BY id_profissional, dia_semana, hora_inicio
    """)
    jornadas = cursor.fetchall()

    cursor.close()
    conexao.close()
    return jornadas
