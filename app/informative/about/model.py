from database import conect_database


def garantir_linha():
    """Cria a linha única se a tabela estiver vazia (telefone NOT NULL, passa '')."""
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM contato")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO contato (telefone) VALUES (%s)", ("",))
        conexao.commit()
    cursor.close()
    conexao.close()


def obter_contato():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, telefone, whatsapp, email, rede_social, endereco FROM contato LIMIT 1"
    )
    r = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not r:
        return None
    return {
        "id": r[0],
        "telefone": r[1],
        "whatsapp": r[2],
        "email": r[3],
        "rede_social": r[4],
        "endereco": r[5],
    }


def atualizar_contato(id_contato, dados):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE contato
        SET telefone = %s, whatsapp = %s, email = %s, rede_social = %s, endereco = %s
        WHERE id = %s
        """,
        (
            dados.telefone,
            dados.whatsapp,
            dados.email,
            dados.rede_social,
            dados.endereco,
            id_contato,
        ),
    )
    conexao.commit()
    cursor.close()
    conexao.close()