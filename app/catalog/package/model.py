from database import conect_database


def obter_id_profissional_por_usuario(id_usuario):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM profissional WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado[0] if resultado else None


def profissional_existe(id_profissional):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM profissional WHERE id = %s", (id_profissional,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def categoria_existe(id_categoria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM categoria WHERE id = %s", (id_categoria,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def obter_ou_criar_categoria_pacotes():
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id FROM categoria WHERE LOWER(nome) = 'pacotes'")
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute(
            "INSERT INTO categoria (nome, ativo) VALUES ('Pacotes', TRUE) RETURNING id"
        )
        id_cat = cursor.fetchone()[0]
        conexao.commit()
        return id_cat
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def subservico_existe(id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM subservico WHERE id = %s", (id_subservico,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def subservico_no_portfolio(id_profissional, id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT 1 FROM profissional_subservico WHERE id_profissional = %s AND id_subservico = %s",
        (id_profissional, id_subservico),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def categoria_do_subservico(id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT c.id FROM subservico sub
        JOIN servico s ON sub.id_servico = s.id
        JOIN categoria c ON s.id_categoria = c.id
        WHERE sub.id = %s
        """,
        (id_subservico,),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado[0] if resultado else None


def obter_info_subservico(id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT sub.nome, s.nome, c.nome
        FROM subservico sub
        JOIN servico s ON sub.id_servico = s.id
        JOIN categoria c ON s.id_categoria = c.id
        WHERE sub.id = %s
        """,
        (id_subservico,),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado


def inserir_vinculo_placeholder(id_profissional, id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO profissional_subservico (id_profissional, id_subservico, preco, duracao_minutos)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id_profissional, id_subservico) DO NOTHING
        """,
        (id_profissional, id_subservico, 0.01, 1),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def obter_ou_criar_servico_pacotes():
    id_categoria = obter_ou_criar_categoria_pacotes()
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT id FROM servico WHERE LOWER(nome) = 'geral' AND id_categoria = %s",
            (id_categoria,),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute(
            "INSERT INTO servico (nome, id_categoria, ativo) VALUES ('Geral', %s, TRUE) RETURNING id",
            (id_categoria,),
        )
        id_serv = cursor.fetchone()[0]
        conexao.commit()
        return id_serv
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def criar_subservico_pacote(nome):
    id_servico = obter_ou_criar_servico_pacotes()
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO subservico (nome, id_servico, ativo) VALUES (%s, %s, TRUE) RETURNING id",
            (nome, id_servico),
        )
        id_sub = cursor.fetchone()[0]
        conexao.commit()
        return id_sub
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def criar_pacote_completo(id_categoria, nome, preco, imagem_url, descricao, ativo, id_profissional, itens):
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO pacote (id_categoria, nome, preco, imagem_url, descricao, ativo)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (id_categoria, nome, preco, imagem_url, descricao, ativo),
        )
        id_pacote = cursor.fetchone()[0]

        for item in itens:
            cursor.execute(
                """
                INSERT INTO pacote_item (id_pacote, id_profissional, id_subservico, quantidade)
                VALUES (%s, %s, %s, %s)
                """,
                (id_pacote, id_profissional, item.id_subservico, item.quantidade),
            )

        conexao.commit()
        return id_pacote
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def atualizar_pacote_completo(id_pacote, id_categoria, nome, preco, imagem_url, descricao, ativo, id_profissional, itens):
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            UPDATE pacote
            SET id_categoria = %s, nome = %s, preco = %s, imagem_url = %s,
                descricao = %s, ativo = %s
            WHERE id = %s
            """,
            (id_categoria, nome, preco, imagem_url, descricao, ativo, id_pacote),
        )
        cursor.execute("DELETE FROM pacote_item WHERE id_pacote = %s", (id_pacote,))

        for item in itens:
            cursor.execute(
                """
                INSERT INTO pacote_item (id_pacote, id_profissional, id_subservico, quantidade)
                VALUES (%s, %s, %s, %s)
                """,
                (id_pacote, id_profissional, item.id_subservico, item.quantidade),
            )

        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


PACOTE_SELECT = """
    SELECT p.id, p.id_categoria, c.nome, p.nome, p.preco, p.descricao, p.imagem_url, p.ativo
    FROM pacote p
    JOIN categoria c ON p.id_categoria = c.id
"""


def _row_para_pacote(r):
    return {
        "id": r[0],
        "id_categoria": r[1],
        "nome_categoria": r[2],
        "nome": r[3],
        "preco": float(r[4]),
        "descricao": r[5],
        "imagem_url": r[6],
        "ativo": r[7],
    }


def obter_pacote(id_pacote):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(PACOTE_SELECT + " WHERE p.id = %s", (id_pacote,))
    r = cursor.fetchone()
    cursor.close()
    conexao.close()
    return _row_para_pacote(r) if r else None


def listar_pacotes_por_profissional(id_profissional):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        PACOTE_SELECT
        + """
        WHERE p.id IN (
            SELECT id_pacote FROM pacote_item WHERE id_profissional = %s
        )
        ORDER BY p.nome
        """,
        (id_profissional,),
    )
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [_row_para_pacote(r) for r in resultados]


def listar_todos_pacotes():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(PACOTE_SELECT + " ORDER BY p.nome")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [_row_para_pacote(r) for r in resultados]


def obter_itens_de_pacotes(ids_pacotes):
    if not ids_pacotes:
        return {}
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT
            pi.id_pacote, pi.id, pi.id_profissional, pi.id_subservico,
            sub.nome, s.nome, c.nome,
            pi.quantidade,
            ps.preco, ps.duracao_minutos, ps.imagem_url,
            prof.nome, prof.imagem_url
        FROM pacote_item pi
        JOIN subservico sub ON pi.id_subservico = sub.id
        JOIN servico s ON sub.id_servico = s.id
        JOIN categoria c ON s.id_categoria = c.id
        JOIN profissional_subservico ps
            ON ps.id_profissional = pi.id_profissional
            AND ps.id_subservico = pi.id_subservico
        JOIN profissional prof ON prof.id = pi.id_profissional
        WHERE pi.id_pacote = ANY(%s)
        ORDER BY pi.ordem_exibicao NULLS LAST, pi.id
        """,
        (list(ids_pacotes),),
    )
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()

    por_pacote = {}
    for r in resultados:
        id_pac = r[0]
        por_pacote.setdefault(id_pac, []).append(
            {
                "id": r[1],
                "id_profissional": r[2],
                "id_subservico": r[3],
                "nome_subservico": r[4],
                "nome_servico": r[5],
                "nome_categoria": r[6],
                "quantidade": r[7],
                "preco_unitario": float(r[8]),
                "duracao_minutos": r[9],
                "imagem_url": r[10],
                "nome_profissional": r[11],
                "imagem_profissional_url": r[12],
            }
        )
    return por_pacote


def verificar_dono(id_pacote, id_profissional):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT 1 FROM pacote_item WHERE id_pacote = %s AND id_profissional = %s",
        (id_pacote, id_profissional),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def contar_pacotes_usando_vinculo(id_profissional, id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT COUNT(DISTINCT id_pacote) FROM pacote_item WHERE id_profissional = %s AND id_subservico = %s",
        (id_profissional, id_subservico),
    )
    total = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return total


def contar_impacto_delete(id_pacote):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM pacote_item WHERE id_pacote = %s", (id_pacote,))
    itens = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM agendamento WHERE id_pacote = %s", (id_pacote,))
    agendamentos = cursor.fetchone()[0]

    cursor.close()
    conexao.close()
    return {"itens": itens, "agendamentos": agendamentos}


def deletar_pacote(id_pacote):
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM pacote_item WHERE id_pacote = %s", (id_pacote,))
        cursor.execute("DELETE FROM pacote WHERE id = %s", (id_pacote,))
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()