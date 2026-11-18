from database import conect_database


def obter_id_profissional_por_usuario(id_usuario):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM profissional WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado[0] if resultado else None


def criar_perfil_basico(id_usuario):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO profissional (id_usuario, nome) VALUES (%s, %s) RETURNING id",
        (id_usuario, "Admin")
    )
    id_prof = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    return id_prof


def verificar_vinculo_existente(id_profissional, id_subservico):
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


def inserir_vinculo(id_profissional, id_subservico, imagem_url, preco, duracao_minutos, descricao):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO profissional_subservico
            (id_profissional, id_subservico, imagem_url, preco, duracao_minutos, descricao)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (id_profissional, id_subservico, imagem_url, preco, duracao_minutos, descricao),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


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


def obter_vinculo(id_profissional, id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT imagem_url, preco, duracao_minutos, ativo, descricao
        FROM profissional_subservico
        WHERE id_profissional = %s AND id_subservico = %s
        """,
        (id_profissional, id_subservico),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not resultado:
        return None
    return {
        "imagem_url": resultado[0],
        "preco": float(resultado[1]),
        "duracao_minutos": resultado[2],
        "ativo": resultado[3],
        "descricao": resultado[4],
    }


def atualizar_vinculo(id_profissional, id_subservico, imagem_url, preco, duracao_minutos, ativo, descricao):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE profissional_subservico
        SET imagem_url = %s, preco = %s, duracao_minutos = %s, ativo = %s, descricao = %s
        WHERE id_profissional = %s AND id_subservico = %s
        """,
        (imagem_url, preco, duracao_minutos, ativo, descricao, id_profissional, id_subservico),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_vinculo(id_profissional, id_subservico):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "DELETE FROM profissional_subservico WHERE id_profissional = %s AND id_subservico = %s",
        (id_profissional, id_subservico),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def listar_por_profissional(id_profissional):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT ps.id_profissional, ps.id_subservico,
               sub.nome, s.nome, c.nome,
               ps.imagem_url, ps.preco, ps.duracao_minutos, ps.ativo, ps.descricao
        FROM profissional_subservico ps
        JOIN subservico sub ON ps.id_subservico = sub.id
        JOIN servico s ON sub.id_servico = s.id
        JOIN categoria c ON s.id_categoria = c.id
        WHERE ps.id_profissional = %s
        ORDER BY s.nome, sub.nome
        """,
        (id_profissional,),
    )
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [
        {
            "id_profissional": r[0],
            "id_subservico": r[1],
            "nome_subservico": r[2],
            "nome_servico": r[3],
            "nome_categoria": r[4],
            "imagem_url": r[5],
            "preco": float(r[6]),
            "duracao_minutos": r[7],
            "ativo": r[8],
            "descricao": r[9],
        }
        for r in resultados
    ]