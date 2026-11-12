from database import conect_database


def inserir_servico(nome, id_categoria, imagem_url):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO servico (nome, id_categoria, imagem_url) VALUES (%s, %s, %s) RETURNING id",
        (nome, id_categoria, imagem_url),
    )
    id_servico = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    return id_servico


def verificar_servico_existente(nome, id_categoria, ignorar_id=None):
    conexao = conect_database()
    cursor = conexao.cursor()
    if ignorar_id:
        cursor.execute(
            "SELECT id FROM servico WHERE LOWER(nome) = LOWER(%s) AND id_categoria = %s AND id <> %s",
            (nome, id_categoria, ignorar_id),
        )
    else:
        cursor.execute(
            "SELECT id FROM servico WHERE LOWER(nome) = LOWER(%s) AND id_categoria = %s",
            (nome, id_categoria),
        )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def obter_nome_categoria(id_categoria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM categoria WHERE id = %s", (id_categoria,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado[0] if resultado else None


def obter_servico(id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, id_categoria, imagem_url, ativo FROM servico WHERE id = %s",
        (id_servico,),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not resultado:
        return None
    return {
        "id": resultado[0],
        "nome": resultado[1],
        "id_categoria": resultado[2],
        "imagem_url": resultado[3],
        "ativo": resultado[4],
    }


def atualizar_servico(id_servico, nome, id_categoria, imagem_url, ativo):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE servico SET nome = %s, id_categoria = %s, imagem_url = %s, ativo = %s WHERE id = %s",
        (nome, id_categoria, imagem_url, ativo, id_servico),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def listar_servicos(id_categoria=None):
    conexao = conect_database()
    cursor = conexao.cursor()
    base = """
        SELECT s.id, s.nome, s.id_categoria, s.imagem_url, s.ativo, c.nome
        FROM servico s
        JOIN categoria c ON s.id_categoria = c.id
    """
    if id_categoria:
        cursor.execute(base + " WHERE s.id_categoria = %s ORDER BY s.nome", (id_categoria,))
    else:
        cursor.execute(base + " ORDER BY c.nome, s.nome")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [
        {
            "id": r[0],
            "nome": r[1],
            "id_categoria": r[2],
            "imagem_url": r[3],
            "ativo": r[4],
            "nome_categoria": r[5],
        }
        for r in resultados
    ]


def contar_impacto_delete(id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM subservico WHERE id_servico = %s", (id_servico,))
    subservicos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM profissional_subservico ps
        JOIN subservico sub ON ps.id_subservico = sub.id
        WHERE sub.id_servico = %s
    """, (id_servico,))
    vinculos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT ps.id_profissional) FROM profissional_subservico ps
        JOIN subservico sub ON ps.id_subservico = sub.id
        WHERE sub.id_servico = %s
    """, (id_servico,))
    profissionais = cursor.fetchone()[0]

    cursor.close()
    conexao.close()
    return {
        "profissionais_afetadas": profissionais,
        "subservicos_afetados": subservicos,
        "vinculos_afetados": vinculos,
    }


def deletar_servico(id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM servico WHERE id = %s", (id_servico,))
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_servico_forcado(id_servico):
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            DELETE FROM agendamento WHERE (id_profissional, id_subservico) IN (
                SELECT ps.id_profissional, ps.id_subservico
                FROM profissional_subservico ps
                JOIN subservico sub ON ps.id_subservico = sub.id
                WHERE sub.id_servico = %s
            )
        """, (id_servico,))

        # Retorna ids de pacotes que tinham itens com subserviços deste serviço
        cursor.execute("""
            DELETE FROM pacote_item WHERE (id_profissional, id_subservico) IN (
                SELECT ps.id_profissional, ps.id_subservico
                FROM profissional_subservico ps
                JOIN subservico sub ON ps.id_subservico = sub.id
                WHERE sub.id_servico = %s
            ) RETURNING id_pacote
        """, (id_servico,))
        ids_pacotes_afetados = list({row[0] for row in cursor.fetchall()})

        cursor.execute("""
            DELETE FROM profissional_subservico WHERE (id_profissional, id_subservico) IN (
                SELECT ps.id_profissional, ps.id_subservico
                FROM profissional_subservico ps
                JOIN subservico sub ON ps.id_subservico = sub.id
                WHERE sub.id_servico = %s
            )
        """, (id_servico,))

        # Pacotes que ficaram sem itens viram órfãos → remove
        if ids_pacotes_afetados:
            cursor.execute("""
                DELETE FROM pacote
                WHERE id = ANY(%s)
                AND id NOT IN (SELECT DISTINCT id_pacote FROM pacote_item)
            """, (ids_pacotes_afetados,))

        cursor.execute("DELETE FROM servico WHERE id = %s", (id_servico,))
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()