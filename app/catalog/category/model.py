from database import conect_database


def inserir_categoria(nome):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO categoria (nome) VALUES (%s) RETURNING id",
        (nome,),
    )
    id_categoria = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    return id_categoria


def verificar_categoria_existente(nome):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM categoria WHERE LOWER(nome) = LOWER(%s)", (nome,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def listar_categorias():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, ativo FROM categoria ORDER BY nome")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [{"id": r[0], "nome": r[1], "ativo": r[2]} for r in resultados]


def obter_categoria(id_categoria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, ativo FROM categoria WHERE id = %s", (id_categoria,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not resultado:
        return None
    return {"id": resultado[0], "nome": resultado[1], "ativo": resultado[2]}


def buscar_por_nome(nome):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM categoria WHERE LOWER(nome) = LOWER(%s)", (nome,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return {"id": resultado[0]} if resultado else None


def atualizar_categoria(id_categoria, nome, ativo):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE categoria SET nome = %s, ativo = %s WHERE id = %s",
        (nome, ativo, id_categoria),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def contar_impacto_delete(id_categoria):
    """Retorna quantos registros serão afetados se deletar a categoria."""
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM servico WHERE id_categoria = %s", (id_categoria,))
    servicos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM subservico sub
        JOIN servico s ON sub.id_servico = s.id
        WHERE s.id_categoria = %s
    """, (id_categoria,))
    subservicos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM profissional_subservico ps
        JOIN subservico sub ON ps.id_subservico = sub.id
        JOIN servico s ON sub.id_servico = s.id
        WHERE s.id_categoria = %s
    """, (id_categoria,))
    vinculos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT ps.id_profissional) FROM profissional_subservico ps
        JOIN subservico sub ON ps.id_subservico = sub.id
        JOIN servico s ON sub.id_servico = s.id
        WHERE s.id_categoria = %s
    """, (id_categoria,))
    profissionais = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    return {
        "profissionais_afetadas": profissionais,
        "servicos_afetados": servicos,
        "subservicos_afetados": subservicos,
        "vinculos_afetados": vinculos,
    }


def deletar_categoria(id_categoria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM categoria WHERE id = %s", (id_categoria,))
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_categoria_forcado(id_categoria):
    """
    Deleta categoria apagando TUDO em cascata:
    agendamentos → pacote_itens → profissional_subservico → pacotes → categoria
    """
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        # 1. Agendamentos que dependem dos vínculos
        cursor.execute("""
            DELETE FROM agendamento WHERE (id_profissional, id_subservico) IN (
                SELECT ps.id_profissional, ps.id_subservico
                FROM profissional_subservico ps
                JOIN subservico sub ON ps.id_subservico = sub.id
                JOIN servico s ON sub.id_servico = s.id
                WHERE s.id_categoria = %s
            )
        """, (id_categoria,))

        # 2. Pacote_itens que dependem dos vínculos
        cursor.execute("""
            DELETE FROM pacote_item WHERE (id_profissional, id_subservico) IN (
                SELECT ps.id_profissional, ps.id_subservico
                FROM profissional_subservico ps
                JOIN subservico sub ON ps.id_subservico = sub.id
                JOIN servico s ON sub.id_servico = s.id
                WHERE s.id_categoria = %s
            )
        """, (id_categoria,))

        # 3. Vínculos profissional_subservico
        cursor.execute("""
            DELETE FROM profissional_subservico WHERE (id_profissional, id_subservico) IN (
                SELECT ps.id_profissional, ps.id_subservico
                FROM profissional_subservico ps
                JOIN subservico sub ON ps.id_subservico = sub.id
                JOIN servico s ON sub.id_servico = s.id
                WHERE s.id_categoria = %s
            )
        """, (id_categoria,))

        # 3.5 Pacotes da categoria (FK pacote.id_categoria é RESTRICT)
        cursor.execute("""
            DELETE FROM pacote_item WHERE id_pacote IN (
                SELECT id FROM pacote WHERE id_categoria = %s
            )
        """, (id_categoria,))
        cursor.execute("DELETE FROM pacote WHERE id_categoria = %s", (id_categoria,))

        # 4. Categoria (CASCADE apaga servico + subservico + carrossel)
        cursor.execute("DELETE FROM categoria WHERE id = %s", (id_categoria,))

        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()