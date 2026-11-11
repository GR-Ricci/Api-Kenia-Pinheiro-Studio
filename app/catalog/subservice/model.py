from database import conect_database


def inserir_subservico(nome, id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO subservico (nome, id_servico) VALUES (%s, %s) RETURNING id",
        (nome, id_servico),
    )
    id_sub = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    return id_sub


def verificar_subservico_existente(nome, id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id FROM subservico WHERE LOWER(nome) = LOWER(%s) AND id_servico = %s",
        (nome, id_servico),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def obter_info_servico(id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT s.nome, c.nome
        FROM servico s
        JOIN categoria c ON s.id_categoria = c.id
        WHERE s.id = %s
        """,
        (id_servico,),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado


def listar_subservicos(id_servico=None):
    conexao = conect_database()
    cursor = conexao.cursor()
    base = """
        SELECT sub.id, sub.nome, sub.id_servico, sub.ativo, s.nome, c.nome
        FROM subservico sub
        JOIN servico s ON sub.id_servico = s.id
        JOIN categoria c ON s.id_categoria = c.id
    """
    if id_servico:
        cursor.execute(base + " WHERE sub.id_servico = %s ORDER BY sub.nome", (id_servico,))
    else:
        cursor.execute(base + " ORDER BY s.nome, sub.nome")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [
        {
            "id": r[0],
            "nome": r[1],
            "id_servico": r[2],
            "ativo": r[3],
            "nome_servico": r[4],
            "nome_categoria": r[5],
        }
        for r in resultados
    ]